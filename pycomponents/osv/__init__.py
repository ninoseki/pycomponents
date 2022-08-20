from functools import lru_cache
from typing import Any, Dict, Optional, cast

import httpx
from cachetools import TTLCache, cached

from pycomponents import settings
from pycomponents.exceptions import OSVQueryException
from pycomponents.utils import make_http_request

from .schemas import Response


class OSV:
    def __init__(self):
        self.base_url = "https://api.osv.dev"

    def _url_for(self, path: str) -> str:
        return self.base_url + path

    def _post(
        self,
        path: str,
        json=Dict[Any, Any],
        *,
        headers: Optional[Dict[Any, Any]] = None
    ) -> httpx.Response:
        url = self._url_for(path)

        return make_http_request(
            url=url,
            method="POST",
            json=json,
            headers=headers,
            timeout=settings.CVE_SEARCH_TIMEOUT,
        )

    @cached(cache=TTLCache(maxsize=settings.OSV_CACHE_SIZE, ttl=settings.OSV_CACHE_TTL))
    def query(self, *, name: str, version: str) -> Response:
        name = name.lower()
        try:
            res = self._post(
                "/v1/query",
                json={
                    "version": version,
                    "package": {"name": name, "ecosystem": "PyPI"},
                },
            )
        except httpx.HTTPError as e:
            raise OSVQueryException(e)

        obj = cast(Dict[Any, Any], res.json())
        return Response.parse_obj(obj)


@lru_cache(maxsize=1)
def get_osv():
    return OSV()
