from typing import Any, Dict, Optional, cast

import httpx

from pycomponents.exceptions import OSVQueryException

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

        res = httpx.post(url, json=json, headers=headers)
        res.raise_for_status()

        return res

    def query(self, *, name: str, version: str) -> Response:
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
