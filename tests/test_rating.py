import pytest

from pycomponents.osv.schemas import Severity
from pycomponents.rating import severity_to_rating


@pytest.fixture
def severity():
    return Severity(
        type="CVSS_V3", score="CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N"
    )


def test_severity_to_rating(severity: Severity):
    rating = severity_to_rating(severity)
    assert rating.score == 8.6
    assert rating.severity == "High"
