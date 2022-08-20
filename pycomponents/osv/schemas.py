from typing import List, Optional

from pydantic import BaseModel, Field


class Reference(BaseModel):
    type: str
    url: str


class Package(BaseModel):
    name: str
    ecosystem: str
    purl: str


class Event(BaseModel):
    introduced: Optional[str] = None
    fixed: Optional[str] = None


class Range(BaseModel):
    type: str
    events: List[Event] = Field(default_factory=list)
    repo: Optional[str] = None


class DatabaseSpecific(BaseModel):
    source: str


class AffectedItem(BaseModel):
    package: Package
    ranges: List[Range] = Field(default_factory=list)
    versions: List[str] = Field(default_factory=list)
    database_specific: DatabaseSpecific


class Vuln(BaseModel):
    id: str
    details: str
    aliases: List[str] = Field(default_factory=list)
    modified: str
    published: str
    references: List[Reference] = Field(default_factory=list)
    affected: List[AffectedItem] = Field(default_factory=list)
    schema_version: str

    @property
    def cve_id(self) -> Optional[str]:
        for alias in self.aliases:
            if alias.startswith("CVE-"):
                return alias

        return None


class Response(BaseModel):
    vulns: List[Vuln] = Field(default_factory=list)
