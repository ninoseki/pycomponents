from typing import List

import psutil
from cyclonedx.model import ExternalReference, ExternalReferenceType, Tool, XsUri
from cyclonedx.model.bom import Bom, Property
from cyclonedx.model.component import Component

from . import constants
from .components import ComponentsFactory
from .service import ServiceFactory
from .site_packages import get_site_packages
from .utils import get_version


def get_external_references() -> List[ExternalReference]:
    return [
        ExternalReference(
            reference_type=ExternalReferenceType.VCS, url=XsUri(constants.vcs_url)
        ),
        ExternalReference(
            reference_type=ExternalReferenceType.DISTRIBUTION,
            url=XsUri(constants.distribution_url),
        ),
    ]


def get_tool() -> Tool:
    version = get_version()
    external_references = get_external_references()
    return Tool(
        vendor=constants.vendor,
        name=constants.name,
        version=version,
        external_references=external_references,
    )


class BOMFactory:
    @staticmethod
    def from_components(components: List[Component]) -> Bom:
        bom = Bom(components=components)

        tool = get_tool()
        bom.metadata.tools.add(tool)

        return bom

    @staticmethod
    def from_process(process: psutil.Process) -> Bom:
        site_packages = get_site_packages(process)
        components = ComponentsFactory.from_site_packages(site_packages)

        bom = BOMFactory.from_components(components)

        service = ServiceFactory.from_process(process)
        for site_package in site_packages:
            service.properties.add(Property(name="site_package", value=site_package))

        bom.services.add(service)

        return bom
