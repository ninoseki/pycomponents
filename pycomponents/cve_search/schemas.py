from typing import Optional

from pydantic import BaseModel, Field


class Response(BaseModel):
    cvss: Optional[float] = Field(None)

    @property
    def severity(self) -> Optional[str]:
        if self.cvss is None:
            return None

        # since it is impossible to determine whether the score based on CVSS v2 or v3,
        # use CVSS v2's scale
        if self.cvss >= 7.0:
            return "High"

        if self.cvss >= 4.0:
            return "Medium"

        return "Low"
