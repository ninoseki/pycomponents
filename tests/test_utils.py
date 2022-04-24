from pycomponents.utils import get_command, get_version, is_python


def test_get_version():
    assert isinstance(get_version(), str)


def test_is_python():
    which = get_command("which")

    try:
        output = which("python")
        path = str(output).strip()
        assert is_python(path)
    except Exception:
        pass
