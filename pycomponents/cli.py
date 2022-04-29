import enum
import os

import typer
from cyclonedx.output import OutputFormat

from .bom import BOMFactory
from .output import OutputFactory
from .processes import get_py_processes

app = typer.Typer()


@enum.unique
class _CLI_OUTPUT_FORMAT(enum.Enum):
    XML = "xml"
    JSON = "json"


_output_formats = {
    _CLI_OUTPUT_FORMAT.XML: OutputFormat.XML,
    _CLI_OUTPUT_FORMAT.JSON: OutputFormat.JSON,
}


def validate_output_dir(output_dir: str) -> bool:
    if not os.path.isdir(output_dir):
        raise ValueError(f"{output_dir} is not a directory")

    return True


@app.command()
def generate_bom(
    output_format: _CLI_OUTPUT_FORMAT = typer.Argument(
        "json", help="The output format for your SBOM (default: json)"
    ),
    output_dir: str = typer.Argument("./", help="The output directory"),
    allow_overwrite: bool = typer.Argument(
        True,
        help="Whether to allow overwriting if the same file exists. (default: True)",
    ),
):
    validate_output_dir(output_dir)

    processes = get_py_processes()
    for process in processes:
        bom = BOMFactory.from_process(process)
        output = OutputFactory.from_bom(
            bom, output_format=_output_formats[output_format]
        )

        filename = os.path.join(
            output_dir, f"pycomponents-{process.pid}.{output_format.value}"
        )
        output.output_to_file(filename, allow_overwrite=allow_overwrite)


if __name__ == "__main__":
    app()
