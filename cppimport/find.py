import os
import sys

import cppimport.config


def find_module_cpppath(modulename, opt_in=False):
    filepath = _find_module_cpppath(modulename, opt_in)
    if filepath is None:
        raise ImportError(
            "Couldn't find a file matching the module name: "
            + str(modulename)
            + "  (opt_in = "
            + str(opt_in)
            + ")"
        )
    return filepath


def _find_module_cpppath(modulename, opt_in=False):
    modulepath_without_ext = modulename.replace(".", os.sep)
    moduledir = os.path.dirname(modulepath_without_ext + ".throwaway")
    matching_dirs = find_matching_path_dirs(moduledir)
    abs_matching_dirs = make_dirs_absolute(matching_dirs)

    for ext in cppimport.config.file_exts:
        modulefilename = os.path.basename(modulepath_without_ext + ext)
        outfilename = find_file_in_folders(modulefilename, abs_matching_dirs, opt_in)
        if outfilename is not None:
            return outfilename

    return None


def make_dirs_absolute(dirs):
    out = []
    for d in dirs:
        if d == "":
            d = os.getcwd()
        if not os.path.isabs(d):
            d = os.path.join(os.getcwd(), d)
        out.append(d)
    return out


def find_matching_path_dirs(moduledir):
    if moduledir == "":
        return sys.path

    ds = []
    for dir in sys.path:
        test_path = os.path.join(dir, moduledir)
        if os.path.exists(test_path) and os.path.isdir(test_path):
            ds.append(test_path)
    return ds


def find_file_in_folders(filename, paths, opt_in):
    for d in paths:
        if not os.path.exists(d):
            continue

        if os.path.isfile(d):
            continue

        for f in os.listdir(d):
            if f != filename:
                continue
            filepath = os.path.join(d, f)
            if opt_in and not check_first_line_contains_cppimport(filepath):
                continue
            return filepath
    return None


def check_first_line_contains_cppimport(filepath):
    with open(filepath, "r") as f:
        return "cppimport" in f.readline()
