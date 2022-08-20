# pycomponents

[![PyPI version](https://badge.fury.io/py/py-sbom-components.svg)](https://badge.fury.io/py/py-sbom-components)
[![Python CI](https://github.com/ninoseki/pycomponents/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/pycomponents/actions/workflows/test.yml)

An experimental tool to generate CycloneDX SBOM from running Python processes.

## Requirements

- Linux and macOS (not tested with Windows)
- Python 3.8+ (tested with Python 3.8, 3.9 and 3.10)

## Installation

```bash
pip install py-sbom-components
```

Note: Initially I planned to publish this tool as `pycomponents`. But it is prohibited by the following restriction.

```
HTTP Error 400: The name 'pycomponents' is too similar to an existing project. See https://pypi.org/help/#project-name for more information.
```

Thus, I use this a little bit lengthy name.

## Usage

```bash
$ pycomponents --help
Usage: pycomponents [OPTIONS]

Options:
  --output-format [xml|json]      The output format for your SBOM  [default:
                                  json]
  --output-dir TEXT               The output directory  [default: ./]
  --allow-overwrite / --no-allow-overwrite
                                  Whether to allow overwriting if the same
                                  file exists  [default: allow-overwrite]
  --exclude-pids INTEGER          A list of pids to exclude
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Example

See [example](https://github.com/ninoseki/pycomponents/tree/main/example).

## What is the difference from `cyclonedx-bom`?

[cyclonedx-bom](https://github.com/CycloneDX/cyclonedx-python)'s BOM comes from:
- Python Environment
- Project's manifest (e.g. Pipfile.lock, poetry.lock or requirements.txt)

`pycomponents` uses a different approach to generate SBOM.

- List up Python processes
- Generate components based on site packages used by Python processes
- Generate vulnerabilities in components by using [OSV](https://osv.dev/) and [cve-search](https://www.cve-search.org/)

Thus `pycomponents` generates half-and-half mixed runtime & static SBOM.
