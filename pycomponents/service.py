from typing import List

import psutil
from cyclonedx.model.service import Property, Service
from psutil._common import pconn


def get_listen_connections(process: psutil.Process, *, kind="tcp"):
    return [
        conn
        for conn in process.connections(kind=kind)
        if conn.status == psutil.CONN_LISTEN
    ]


def convert_to_endpoints(connections: List[pconn], *, kind="tcp") -> List[str]:
    endpoints: List[str] = []
    for conn in connections:
        ip, port = conn.laddr
        endpoints.append(f"{kind}://{ip}:{port}")

        try:
            ip, port = conn.raddr
            endpoints.append(f"{kind}://{ip}:{port}")
        except ValueError:
            pass

    return endpoints


def get_endpoints(process: psutil.Process, *, kind="tcp"):
    try:
        connections = get_listen_connections(process, kind=kind)
        return convert_to_endpoints(connections, kind=kind)
    except Exception:
        return []


def get_tcp_endpoints(process: psutil.Process):
    return get_endpoints(process, kind="tcp")


def get_udp_endpoints(process: psutil.Process):
    return get_endpoints(process, kind="udp")


def get_process_properties(process: psutil.Process) -> List[Property]:
    cmdline = " ".join(process.cmdline())

    properties: List[Property] = [
        Property(name="pid", value=str(process.pid)),
        Property(name="exe", value=process.exe()),
        Property(name="cmdline", value=cmdline),
        Property(name="username", value=process.username()),
    ]

    try:
        properties.append(Property(name="cwd", value=process.cwd()))
    except Exception:
        pass

    return properties


class ServiceFactory:
    @staticmethod
    def from_process(process: psutil.Process) -> Service:
        service = Service(name=str(process.pid))

        service.endpoints.update(get_tcp_endpoints(process))
        service.endpoints.update(get_udp_endpoints(process))

        properties = get_process_properties(process)
        for prop in properties:
            service.properties.add(prop)

        return service
