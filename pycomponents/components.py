import pkg_resources
from cyclonedx.model import LicenseChoice
from cyclonedx.model.component import Component, Property
from importlib_metadata import PackageMetadata as _MetadataReturn
from importlib_metadata import PackageNotFoundError, metadata
from packageurl import PackageURL


def _get_metadata_for_package(package_name: str) -> _MetadataReturn:
    return metadata(package_name)


class ComponentFactory:
    @staticmethod
    def from_dist(dist: pkg_resources.Distribution):
        c = Component(
            name=dist.project_name,
            version=dist.version,
            purl=PackageURL(type="pypi", name=dist.project_name, version=dist.version),
            properties=[
                Property(name="location", value=dist.location),
            ],
        )

        try:
            i_metadata = _get_metadata_for_package(dist.project_name)
            if "Author" in i_metadata:
                c.author = i_metadata["Author"]

            if "License" in i_metadata and i_metadata["License"] != "UNKNOWN":
                c.licenses.add(LicenseChoice(license_expression=i_metadata["License"]))

            if "Classifier" in i_metadata:
                for classifier in i_metadata["Classifier"]:
                    if str(classifier).startswith("License :: OSI Approved :: "):
                        c.licenses.add(
                            LicenseChoice(
                                license_expression=str(classifier)
                                .replace("License :: OSI Approved :: ", "")
                                .strip()
                            )
                        )
        except PackageNotFoundError:
            pass

        return c


class ComponentsFactory:
    @staticmethod
    def from_site_package(site_package: str) -> list[Component]:
        components: list[Component] = []
        for dist in pkg_resources.find_distributions(site_package):
            components.append(ComponentFactory.from_dist(dist))

        return components

    @staticmethod
    def from_site_packages(site_packages: set[str]) -> list[Component]:
        components: list[Component] = []
        for site_package in site_packages:
            components.extend(ComponentsFactory.from_site_package(site_package))

        return components
