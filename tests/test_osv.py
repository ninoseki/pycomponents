import pytest
import vcr

from pycomponents.exceptions import OSVQueryException
from pycomponents.osv import OSV


@vcr.use_cassette("tests/fixtures/vcr_cassettes/osv_jinja2_2.4.1.yaml")
def test_query():
    osv = OSV()
    res = osv.query(name="jinja2", version="2.4.1")
    assert len(res.vulns) > 0


@vcr.use_cassette("tests/fixtures/vcr_cassettes/osv_query_no_vulns.yaml")
def test_query_no_vulns():
    osv = OSV()
    res = osv.query(name="jinja2", version="100.0.0")
    assert len(res.vulns) == 0


@vcr.use_cassette("tests/fixtures/vcr_cassettes/osv_400.yaml")
def test_query_error():
    osv = OSV()

    with pytest.raises(OSVQueryException) as e:
        osv.query(name=-1, version=-1)

        assert "400 Bad Request" in str(e)
