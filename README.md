# pycomponents

An experimental tool to generate CycloneDX SBOM from running Python processes.

## What is the difference from `cyclonedx-bom`?

[cyclonedx-bom](https://github.com/CycloneDX/cyclonedx-python)'s BOM comes from:
- Python Environment
- Project's manifest (e.g. Pipfile.lock, poetry.lock or requirements.txt)

`pycomponents` uses a different approach to generate SBOM.

- List up Python processes
- Inspect site packages used by a process
- Generate SBOM based on site packages

Thus `pycomponents` generates half-and-half mixed runtime & static SBOM.
