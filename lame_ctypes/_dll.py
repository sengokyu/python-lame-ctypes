"""
Following code is derived from 
[python-openal](https://pypi.org/project/python-openal/)
"""
import os
import sys
import ctypes
import warnings
from ctypes.util import find_library

_extensions = {
    "win32": ".dll",
    "cli": ".dll",
    "darwin": ".dylib"
}


def _findlib(libnames, path=None):
    """Internal helper function to find the requested DLL(s)."""
    platform = sys.platform
    suffix = ".so" if platform not in _extensions else _extensions[platform]
    searchfor = libnames["DEFAULT"] if platform not in libnames else libnames[platform]

    results = []
    if path:
        for libname in searchfor:
            dllfile = os.path.join(path, "%s%s" % (libname, suffix))
            if os.path.exists(dllfile):
                results.append(dllfile)
    for libname in searchfor:
        dllfile = find_library(libname)
        if dllfile:
            results.append(dllfile)
    return results


class dll(object):
    """Function wrapper around the different DLL functions. Do not use or
    instantiate this one directly from your user code.
    """

    def __init__(self, libinfo, libnames, path=None):
        self._dll = None
        foundlibs = _findlib(libnames, path)
        if len(foundlibs) == 0:
            raise RuntimeError("could not find any library for %s" % libinfo)
        for libfile in foundlibs:
            try:
                self._dll = ctypes.CDLL(libfile)
                self._libfile = libfile
                break
            except Exception as exc:
                # Could not load it, silently ignore that issue and move
                # to the next one.
                warnings.warn(exc, ImportWarning)
        if self._dll is None:
            raise RuntimeError("could not load any library for %s" % libinfo)

    def bind_function(self, funcname, args=None, returns=None):
        """Binds the passed argument and return value types to the specified
        function."""
        func = getattr(self._dll, funcname)
        func.argtypes = args
        func.restype = returns
        return func
