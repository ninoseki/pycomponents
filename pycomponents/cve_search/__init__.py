from functools import lru_cache
from typing import Any, Dict, cast

import httpx
from cachetools import TTLCache, cached

from pycomponents import settings
from pycomponents.exceptions import CVESearchQueryException
from pycomponents.utils import make_http_request

from .schemas import Response


class CVESearch:
    def __init__(self):
        self.base_url = "https://cve.circl.lu"

    def _url_for(self, path: str) -> str:
        return self.base_url + path

    def _get(
        self,
        path: str,
    ) -> httpx.Response:
        url = self._url_for(path)

        return make_http_request(
            url=url, method="GET", timeout=settings.CVE_SEARCH_TIMEOUT
        )

    @cached(
        cache=TTLCache(
            maxsize=settings.CVE_SEARCH_CACHE_SIZE, ttl=settings.CVE_SEARCH_CACHE_TTL
        )
    )
    def query(self, cve_id) -> Response:
        try:
            res = self._get(
                f"/api/cve/{cve_id}",
            )
        except httpx.HTTPError as e:
            raise CVESearchQueryException(e)

        obj = cast(Dict[Any, Any], res.json())
        return Response.parse_obj(obj)


@lru_cache(maxsize=1)
def get_cve_search():
    return CVESearch()
