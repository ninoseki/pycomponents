import enum

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


@app.command()
def generate_bom(
    output_format: _CLI_OUTPUT_FORMAT = "json",
    allow_overwrite: bool = True,
):
    processes = get_py_processes()
    for process in processes:
        bom = BOMFactory.from_process(process)
        output = OutputFactory.from_bom(
            bom, output_format=_output_formats[output_format]
        )

        filename = f"pycomponents-{process.pid}.{output_format.value}"
        output.output_to_file(filename, allow_overwrite=allow_overwrite)


if __name__ == "__main__":
    app()
