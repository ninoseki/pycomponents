from cyclonedx.model.bom import Bom
from cyclonedx.output import BaseOutput, OutputFormat, get_instance


class OutputFactory:
    @staticmethod
    def from_bom(
        bom: Bom, *, output_format: OutputFormat = OutputFormat.JSON
    ) -> BaseOutput:
        return get_instance(bom, output_format=output_format)
