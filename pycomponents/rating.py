from typing import Optional, Union, cast

from cvss import CVSS2, CVSS3
from cyclonedx.model.vulnerability import VulnerabilityRating

from .cve_search import get_cve_search
from .exceptions import CVESearchQueryException
from .osv.schemas import Severity, Vuln


def severity_to_rating(severity: Severity) -> Optional[VulnerabilityRating]:
    severity_type_to_cvss = {
        "CVSS_V3": CVSS3,
        "CVSS_V2": CVSS2,
    }

    klass = severity_type_to_cvss.get(severity.type)
    if klass is None:
        return None

    c = cast(Union[CVSS2, CVSS3], klass(severity.score))
    score, _, _ = c.scores()
    severity_str, _, _ = c.severities()
    return VulnerabilityRating(score=score, severity=severity_str)


class RatingFactory:
    @staticmethod
    def from_osv_vuln(vuln: Vuln) -> Optional[VulnerabilityRating]:
        rating: Optional[VulnerabilityRating] = None

        if len(vuln.severity) > 0:
            # TODO: consider a case when there are multi severities
            severity = vuln.severity[0]
            rating = severity_to_rating(severity)
            if rating is not None:
                return rating

        if vuln.cve_id is not None:
            try:
                cve_search = get_cve_search()
                res = cve_search.query(vuln.cve_id)
                rating = VulnerabilityRating(score=res.cvss, severity=res.severity)
            except CVESearchQueryException:
                pass

        return rating
