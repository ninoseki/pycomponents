from typing import Optional

from pydantic import BaseModel, Field


class Response(BaseModel):
    cvss: Optional[float] = Field(None)

    @property
    def severity(self) -> Optional[str]:
        if self.cvss is None:
            return None

        if self.cvss >= 7.0:
            return "high"

        if self.cvss >= 4.0:
            return "medium"

        return "low"
