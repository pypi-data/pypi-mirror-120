#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import os
from collections import OrderedDict
from typing import Dict, Any
from functools import partial
from urllib.parse import urljoin

import requests
from cachetools import cached
import logging
from cachetools import TTLCache

from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.models.paginator import Paginator
from dli.client.components.urls import dataset_urls, identity_urls
from dli.models.dataset_model import DatasetModel
from dli.modules.package_module import PackageModule


class DatasetModule:
    """
    DatasetModule contains functions that operate across datasets e.g. searching for a dataset and
    getting a specific dataset.

    Caching was added due to a user calling this in a tight loop, causing load on the Catalogue.
    The default TTL is set to 60 seconds so that users do not have to wait long after changing
    their visible organisation setting to see the change reflected in the SDK, and at the same
    time cutting the load on Catalogue.
    The TTL value come from the environment variable `DLI_CACHE_TTL`. It is overridable for QA
    testing. Users should not override this value unless you are sure that you are not expecting
    the visible organisations list to change while running your code.
    """

    trace_logger = logging.getLogger('trace_logger')

    # Scope is class level so that different calls to `.get` will be using the same cache.
    __visible_orgs_ttl_cache: TTLCache = TTLCache(
        maxsize=16,
        ttl=int(os.environ.get("DLI_CACHE_TTL", '60'))
    )

    def __call__(self, search_term=None, only_mine=False, warn=False, page_size=5000) \
            -> Dict[str, DatasetModel]:
        """
        See datasets.

        :Example:

            Get all datasets (including those you do not yet have access to):

            .. code:: python

                client.datasets()

        :Example:

            Get **only** datasets you have access to and
            can read:

            .. code:: python

                client.datasets(only_mine=True)

        :Example:

            Search for datasets using `ilike`. This will find fields that are
            similar to value. This is recommended over using `like` as it
            performs case insensitive matching. Example usages `ilike example`.

            Some examples of how the logic matches in the database:

            'example' ILIKE 'example'    true

            'example' ILIKE 'ex%'     true

            'example' ILIKE 'c'      false

            .. code:: python

                # Exact match `example` (case sensitive).
                client.datasets(search_term='name=example')

                # Match `example` (case insensitive).
                client.datasets(search_term='name ilike example')

                # Match `example` (case insensitive) followed by any characters.
                client.datasets(search_term='name ilike example%')

                # Match `example` (case insensitive) in the middle of any characters.
                client.datasets(search_term='name ilike %example%')

        :Example:

            Search for datasets with multiple search terms:

            .. code:: python

                client.datasets(
                    search_term=[
                        'name=example',
                        'manager_id=example'
                    ]
                )

        :Example:

            Search for datasets with name and only_mine:

            .. code:: python

                client.datasets(
                    search_term='name=example',
                    only_mine=True,
                )


        :param search_term: search term for dataset. Can filter using a simple
            query language. E.G "field=value", "field>value", "field ilike value".
            Can pass in multiple values using a list of strings.

        :param bool only_mine: Specify whether to collect datasets only
        accessible to you (True) or to discover packages that you may
        want to discover but may not have access to (False).

        :param int page_size: Optional. Default 5000. Used to control the size
        of internal calls from the SDK to the Catalogue. This parameter is
        only exposed to allow performance testing and changes for batch jobs.
        Customers should use the default setting.

        :returns: Ordered dictionary of ids to DatasetModel.
        :rtype: OrderedDict[id: str, DatasetModel]
        """

        filters = {}
        for x in PackageModule._filter_creation(search_term, only_mine):
            filters.update(x)

        p = Paginator(
            dataset_urls.v2_index,
            self._client._DatasetFactory,
            partial(self._client._DatasetFactory._from_v2_response_unsheathed, warn=warn),
            page_size=page_size,
            max_workers=5,
            filters=filters
        )

        results = [(v.short_code, v) for v in p]
        o = OrderedDict()
        for code, val in results:
            if code in o:
                o[code] = [o[code]]
                o[code].append(val)
            else:
                o[code] = val

        return o

    def _visible_orgs(self) -> Dict[Any, Any]:
        """Make a call to the Catalogue."""
        url = urljoin(self._client._environment.catalogue, identity_urls.orgs_visible_to_user)
        self.trace_logger.info(f'visible_orgs: Make real call to Catalogue, url {url}')
        return self._client.session.get(url).json()

    @cached(cache=__visible_orgs_ttl_cache)
    def _visible_orgs_cache_func(self, jwt: str) -> Dict[Any, Any]:
        """
        Do a cache lookup before making a call to the Catalogue.

        :param str jwt: SECURITY: Explicitly tie the cache entry to the JWT. If the JWT
        refreshes then we intend for a cache miss that will trigger a new call to the Catalogue.
        """
        return self._visible_orgs()

    def get(self, short_code, organisation_short_code=None, page_size=5000) -> DatasetModel:
        """
        Returns a DatasetModel if it exists, and a user has access else None

        :param str short_code: The short code of the dataset to collect

        :param organisation_short_code:  The short code of the organisation
        for this dataset

        :param int page_size: Optional. Default 5000. Used to control the size
        of internal calls from the SDK to the Catalogue. This parameter is
        only exposed to allow performance testing and changes for batch jobs.
        Customers should use the default setting.

        :returns: Dataset model with matching short code.
        :rtype: DatasetModel
        """

        search_terms = [
            f"short_code={short_code}"
        ]

        if organisation_short_code is not None:
            search_terms.append(
                f"organisation_short_code={organisation_short_code}"
            )

        # todo - not going to work as expected since the orderdict wont have dups
        results: Dict[str, DatasetModel] = self._client.datasets(search_term=search_terms, only_mine=False, warn=True, page_size=page_size)
        res = results.get(short_code)

        if type(res) is list:
            # Multiple datasets with same shortcode! This can happen as short codes are only
            # unique within an organisation. We need to call Catalogue to tell the user the
            # visible organisations they have access to so that they can make the call again
            # but with the organisation short code so that only one dataset is returned.
            self.trace_logger.debug(f"ttl set to: {self.__visible_orgs_ttl_cache.ttl.real}")
            jwt: str = self._client.session.auth_key
            visible_orgs_response = self._visible_orgs_cache_func(jwt=jwt)

            mapping_to_sc = dict(map(
                lambda x: (x["id"],
                           x["attributes"]["short_code"]
                           ),
                visible_orgs_response["data"])
            )

            if os.name != 'nt':
                org_codes=[f"\033[4m\033[92m\033[1morganisation_short_code=" \
                           f"{mapping_to_sc.get(x.organisation_id, x.organisation_id)}" \
                           f"\033[0;0m -> {x.short_code}"
                           for x in res]

                msg = f"\033[96mMultiple datasets have shortcode: \033[1m`{short_code}`\033[0;0m\n\nShortcodes are"\
                      f" only guaranteed to be unique per organisation, and you seem to "\
                      f" have access to multiple organisation's datasets, where there are "\
                      f"datasets bearing the same shortcode."\
                      f"\n"\
                      f"To resolve this, please specify the organisation_short_code in "\
                      f"the call to datasets.get(shortcode, organisation_short_code=ORG CODE)"\
                      f"\n\nThe available (accessible to you) organisations shortcodes "\
                      f"for this dataset short code are:\n" + ("\n".join(org_codes))
            else:
                org_codes = [f"organisation_short_code=" \
                             f"{mapping_to_sc.get(x.organisation_id, x.organisation_id)}" \
                             f" -> {x.short_code}"
                             for x in res]

                msg = f"Multiple datasets have shortcode: `{short_code}`\n\nShortcodes are" \
                      f" only guaranteed to be unique per organisation, and you seem to " \
                      f" have access to multiple organisation's datasets, where there are " \
                      f"datasets bearing the same shortcode." \
                      f"\n" \
                      f"To resolve this, please specify the organisation_short_code in " \
                      f"the call to datasets.get(shortcode, organisation_short_code=ORG CODE)" \
                      f"\n\nThe available (accessible to you) organisations shortcodes " \
                      f"for this dataset short code are:\n" + (
                          "\n".join(org_codes))

            raise Exception(
                msg
            )

            #todo - difficult here, really need to convert id to shortcode for org
            #todo - else isnt that useful a message as user now needs to discover these
        elif res:
            return res
        else:
            if self._client.strict:
                r = requests.Response()
                r.status_code = 404
                r.request = (lambda: True)
                r.request.method = f"No such dataset {short_code}"
                r.request.url = ""
                raise CatalogueEntityNotFoundException(
                    message=f"No such dataset {short_code}",
                    response=r
                )
            else:
                return None
