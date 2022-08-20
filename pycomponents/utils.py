import os
from functools import lru_cache
from typing import Any, Dict, Optional

import httpx
import sh

from . import __version__


@lru_cache
def get_command(path: str) -> sh.Command:
    return sh.Command(path)


def get_version() -> str:
    return __version__


def is_python(path: str) -> bool:
    if not os.path.isfile(path):
        return False

    name = path.split("/")[-1]
    if not name.startswith("python"):
        return False

    python = get_command(path)
    try:
        output = python("--version")
        return str(output).startswith("Python ")
    except Exception:
        return False


def make_http_request(
    *,
    url: str,
    method: str,
    timeout: int,
    params: Optional[Dict[Any, Any]] = None,
    json: Optional[Dict[Any, Any]] = None,
    headers: Optional[Dict[Any, Any]] = None,
) -> httpx.Response:
    with httpx.Client(timeout=timeout) as client:
        req = httpx.Request(
            method=method, url=url, params=params, json=json, headers=headers
        )
        res = client.send(req)

    res.raise_for_status()

    return res
