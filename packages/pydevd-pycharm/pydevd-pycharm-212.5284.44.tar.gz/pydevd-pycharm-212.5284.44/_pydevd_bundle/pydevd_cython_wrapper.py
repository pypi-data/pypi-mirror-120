import sys

# This version number is always available
from _pydevd_bundle.pydevd_additional_thread_info_regular import version as regular_version

try:
    try:
        from _pydevd_bundle_ext import pydevd_cython as mod

    except ImportError:
        from _pydevd_bundle import pydevd_cython as mod

except ImportError:
    import struct

    try:
        is_python_64bit = (struct.calcsize('P') == 8)
    except:
        # In Jython this call fails, but this is Ok, we don't support Jython for speedups anyways.
        raise ImportError
    plat = '32'
    if is_python_64bit:
        plat = '64'

    # We also accept things as:
    #
    # _pydevd_bundle.pydevd_cython_win32_27_32
    # _pydevd_bundle.pydevd_cython_win32_34_64
    #
    # to have multiple pre-compiled pyds distributed along the IDE
    # (generated by build_tools/build_binaries_windows.py).

    mod_name = 'pydevd_cython_%s_%s%s_%s' % (sys.platform, sys.version_info[0], sys.version_info[1], plat)
    check_name = '_pydevd_bundle.%s' % (mod_name,)
    mod = getattr(__import__(check_name), mod_name)

# Regardless of how it was found, make sure it's later available as the
# initial name so that the expected types from Cython in frame eval
# are valid.
sys.modules['_pydevd_bundle.pydevd_cython'] = mod

# This version number from the already compiled Cython extension
version = getattr(mod, 'version', 0)

if version != regular_version:
    exc = ImportError()
    exc.version_mismatch = True
    raise exc

trace_dispatch = mod.trace_dispatch

PyDBAdditionalThreadInfo = mod.PyDBAdditionalThreadInfo

set_additional_thread_info = mod.set_additional_thread_info

global_cache_skips = mod.global_cache_skips

global_cache_frame_skips = mod.global_cache_frame_skips

_set_additional_thread_info_lock = mod._set_additional_thread_info_lock

fix_top_level_trace_and_get_trace_func = mod.fix_top_level_trace_and_get_trace_func
