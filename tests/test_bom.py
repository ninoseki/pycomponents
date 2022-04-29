from pycomponents import __version__
from pycomponents.bom import get_tool


def test_get_tool():
    tool = get_tool()
    assert tool.vendor == "ninoseki"
    assert tool.name == "pycomponents"
    assert tool.version == __version__
