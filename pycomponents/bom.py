import psutil
from cyclonedx.model import Tool
from cyclonedx.model.bom import Bom, Property
from cyclonedx.model.component import Component

from .components import ComponentsFactory
from .site_packages import get_site_packages
from .utils import get_version


def get_tool() -> Tool:
    version = get_version()
    return Tool(vendor="pycomponents", name="pycomponents-bom", version=version)


def get_process_properties(process: psutil.Process) -> list[Property]:
    cmdline = " ".join(process.cmdline())

    properties: list[Property] = [
        Property(name="pid", value=str(process.pid)),
        Property(name="exe", value=process.exe()),
        Property(name="cmdline", value=cmdline),
    ]

    try:
        properties.append(Property(name="cwd", value=process.cwd()))
    except Exception:
        pass

    return properties


class BOMFactory:
    @staticmethod
    def from_components(components: list[Component]) -> Bom:
        bom = Bom(components=components)

        tool = get_tool()
        bom.metadata.tools.add(tool)

        return bom

    @staticmethod
    def from_process(process: psutil.Process) -> Bom:
        site_packages = get_site_packages(process)
        components = ComponentsFactory.from_site_packages(site_packages)
        bom = BOMFactory.from_components(components)

        properties = get_process_properties(process)
        for prop in properties:
            bom.metadata.properties.add(prop)

        for site_package in site_packages:
            bom.metadata.properties.add(
                Property(name="site_package", value=site_package)
            )

        return bom
