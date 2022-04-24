from typing import List, Optional

import psutil

from .utils import is_python


def is_python_process(process: psutil.Process) -> bool:
    try:
        exe = process.exe()
        return is_python(exe)
    except Exception:
        pass

    return False


def get_process(pid: int) -> Optional[psutil.Process]:
    try:
        return psutil.Process(pid)
    except Exception:
        pass

    return None


def get_py_processes() -> List[psutil.Process]:
    pids = psutil.pids()

    processes: List[psutil.Process] = []
    for pid in pids:
        process = get_process(pid)
        if process is None:
            continue

        if is_python_process(process):
            processes.append(process)

    return processes
