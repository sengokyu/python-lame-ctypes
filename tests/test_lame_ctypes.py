import lame_ctypes


def test_version():
    assert lame_ctypes.__version__ == "0.1.3"


def test_exporting():
    assert hasattr(lame_ctypes, "lame_init")
