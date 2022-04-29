from pycomponents import __version__, constants
from pycomponents.bom import get_tool


def test_get_tool():
    tool = get_tool()
    assert tool.vendor == constants.vendor
    assert tool.name == constants.name
    assert tool.version == __version__
