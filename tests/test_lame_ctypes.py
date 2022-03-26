import lame_ctypes


def test_exporting():
    assert hasattr(lame_ctypes, "lame_init")
