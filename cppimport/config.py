"""
Configuration settings for cppimport.

TODO: This module should be sanitized so that there is a single dictionary of
configuration settings.
"""
import ctypes

should_force_rebuild = False
file_exts = [".cpp", ".c"]
rtld_flags = ctypes.RTLD_LOCAL


def force_rebuild(to=True):
    global should_force_rebuild
    should_force_rebuild = to


def turn_off_strict_prototypes():
    import distutils.sysconfig

    cfg_vars = distutils.sysconfig.get_config_vars()
    for key, value in cfg_vars.items():
        if type(value) == str:
            cfg_vars[key] = value.replace("-Wstrict-prototypes", "")


def set_rtld_flags(flags):
    global rtld_flags
    rtld_flags = flags
