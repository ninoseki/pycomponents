import pytest

from pycomponents.site_packages import get_string_between_quotes


@pytest.mark.parametrize("s,expected", [("'foo' 'bar' '", ["foo", "bar"]), ("''", [])])
def test_get_string_between_quotes(s: str, expected):
    assert get_string_between_quotes(s) == expected
