import os
from functools import lru_cache

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
