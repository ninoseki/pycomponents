import pytest

from pycomponents.cli import validate_output_dir


def test_validate_output_dir():
    assert validate_output_dir("./") is True


def test_validate_output_dir_with_value_error():
    with pytest.raises(ValueError):
        assert validate_output_dir("/tmp/404/not_found")
