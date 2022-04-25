import os
from typing import List, Optional, Set

import psutil

from .utils import get_command, is_python


def get_string_between_quotes(s: str) -> List[str]:
    strings = s.split("'")[1::2]
    return [string for string in strings if string != ""]


def am_i_root() -> bool:
    id = get_command("id")
    try:
        output = id("-u")
        return int(str(output).strip()) == 0
    except Exception:
        return False


def get_python_in_cmdline(process: psutil.Process) -> Optional[str]:
    cmdline = process.cmdline()

    if len(cmdline) == 0:
        return None

    first = cmdline[0]
    if is_python(first):
        return first

    return None


def get_site_packages(process: psutil.Process) -> Set[str]:
    site_packages: Set[str] = set()
    output = None

    # Python may be nested like the following
    exe = get_python_in_cmdline(process) or process.exe()
    user = process.username()

    sys_path_command = "import sys;print(sys.path)"
    if am_i_root():
        sudo = get_command("sudo")
        try:
            c = f'{exe} -c "{sys_path_command}"'
            output = sudo("su", user, "-c", c)
        except Exception:
            return site_packages
    else:
        py = get_command(exe)
        try:
            output = py("-c", sys_path_command)
        except Exception:
            return site_packages

    if output is None:
        return site_packages

    lines = str(output).splitlines()

    for line in lines:
        line = line.strip()
        possible_site_packages = get_string_between_quotes(line)

        for site_package in possible_site_packages:
            if not site_package.endswith("/site-packages"):
                continue

            if not os.path.isdir(site_package):
                continue

            site_packages.add(site_package)

    return set(site_packages)
