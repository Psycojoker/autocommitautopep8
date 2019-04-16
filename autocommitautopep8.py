# encoding: utf-8

import os
import autopep8
import subprocess
import multiprocessing

from collections import OrderedDict

errors = OrderedDict([
    ("E101", "Reindent all lines"),
    ("E11", "Fix indentation"),
    ("E121", "Fix indentation to be a multiple of four"),
    ("E122", "Add absent indentation for hanging indentation"),
    ("E123", "Align closing bracket to match opening bracket"),
    ("E124", "Align closing bracket to match visual indentation"),
    ("E125", "Indent to distinguish line from next logical line"),
    ("E126", "Fix over-indented hanging indentation"),
    ("E127", "Fix visual indentation"),
    # ("E128", "Fix visual indentation"),
    ("E129", "Fix visual indentation"),
    ("E131", "Fix hanging indent for unaligned continuation line"),
    ("E133", "Fix missing indentation for closing bracket"),
    ("E20", "Remove extraneous whitespace"),
    ("E211", "Remove extraneous whitespace"),
    ("E22", "Fix extraneous whitespace around keywords"),
    ("E224", "Remove extraneous whitespace around operator"),
    ("E225", "Fix missing whitespace around operator"),
    ("E226", "Fix missing whitespace around arithmetic operator"),
    ("E227", "Fix missing whitespace around bitwise/shift operator"),
    ("E228", "Fix missing whitespace around modulo operator"),
    ("E231", "Add missing whitespace"),
    ("E241", "Fix extraneous whitespace around keywords"),
    ("E242", "Remove extraneous whitespace around operator"),
    ("E251", "Remove whitespace around parameter \"=\" sign"),
    ("E252", "Missing whitespace around parameter equals"),
    ("E26", "Fix spacing after comment hash for inline comments"),
    ("E265", "Fix spacing after comment hash for block comments"),
    ("E266", "Fix too many leading \"#\" for block comments"),
    ("E27", "Fix extraneous whitespace around keywords"),
    ("E301", "Add missing blank line"),
    ("E302", "Add missing 2 blank lines"),
    ("E303", "Remove extra blank lines"),
    ("E304", "Remove blank line following function decorator"),
    ("E305", "Expected 2 blank lines after end of function or class"),
    ("E306", "Expected 1 blank line before a nested definition"),
    ("E401", "Put imports on separate lines"),
    ("E402", "Fix module level import not at top of file"),
    # ("E501", "Try to make lines fit within --max-line-length characters"),
    ("E502", "Remove extraneous escape of newline"),
    ("E701", "Put colon-separated compound statement on separate lines"),
    ("E70", "Put semicolon-separated compound statement on separate lines"),
    ("E711", "Fix comparison with None"),
    ("E712", "Fix comparison with boolean"),
    ("E713", "Use \"not in\" for test for membership"),
    ("E714", "Use \"is not\" test for object identity"),
    ("E721", "Use \"isinstance()\" instead of comparing types directly"),
    ("E722", "Fix bare except"),
    ("E731", "Use a def when use do not assign a lambda expression"),
    ("W291", "Remove trailing whitespace"),
    ("W292", "Add a single newline at the end of the file"),
    ("W293", "Remove trailing whitespace on blank line"),
    ("W391", "Remove trailing blank lines"),
    # ("W503", "Fix line break before binary operator"),
    ("W504", "Fix line break after binary operator"),
    ("W601", "Use \"in\" rather than \"has_key()\""),
    ("W602", "Fix deprecated form of raising exception"),
    ("W603", "Use \"!=\" instead of \"<>\""),
    ("W604", "Use \"repr()\" instead of backticks"),
    ("W605", "Fix invalid escape sequence \"x\""),
    ("W690", "Fix various deprecated code (via lib2to3)"),
])


def get_python_files():
    ignore_roots = []
    python_files = []

    for root, dirs, files in os.walk("."):
        if root.startswith(tuple(ignore_roots)):
            continue

        if root.split("/")[-1].startswith(".") and root != ".":
            ignore_roots.append(root)
            continue

        if root.endswith((".git", ".hg")):
            ignore_roots.append(root)
            continue

        # ignore virtualenvs
        if {"bin", "include", "lib"}.issubset(set(dirs)):
            ignore_roots.append(root)
            continue

        for file in files:
            file = os.path.join(root, file)
            if file.endswith(".py"):
                python_files.append(file)
            elif not file.endswith((".pyc", ".css", ".js", ".html")):
                content = open(file, "r").read()[:300].lower()

                if "# encoding: utf-8" in content:
                    python_files.append(file)
                elif "#!/usr/bin/env" in content:
                    python_files.append(file)
                elif "#!/usr/bin/python" in content:
                    python_files.append(file)

    return python_files


def _fix_file(parameters):
    """Helper function for optionally running fix_file() in parallel."""
    try:
        result = autopep8.fix_file(*parameters)
        if result:
            print("%s %s" % (parameters[1].select[0], parameters[0]))
        return result
    except IOError as error:
        print(unicode(error))


def fix_multiple_files(filenames, options, output=None):
    """Fix list of files.

    Optionally fix files recursively.

    """

    results = []
    pool = multiprocessing.Pool(options.jobs)
    ret = pool.map_async(_fix_file, [(name, options) for name in filenames])

    # the .get() stuff is to handle KeywordInterrupt because
    # multiprocessing.Pool is broken for that
    results.extend([x for x in ret.get(99999999999999999999999999999) if x])

    return results


class FakeOption:
    in_place = True
    line_range = None
    ignore = []
    max_line_length = None
    hang_closing = False
    aggressive = False
    verbose = False
    pep8_passes = None
    experimental = False
    diff = False
    indent_size = 4
    jobs = max(1, multiprocessing.cpu_count() / 2)
    recursive = False
    exclude = None
    max_line_length = 80


def main():
    python_files = get_python_files()

    options = FakeOption()

    for number, (error, description) in enumerate(errors.items(), start=1):
        options.select = [error]
        if fix_multiple_files(python_files, options=options):
            command = "hg commit -m '[autopep8] {error} - {description}'".format(error=error, description=description)
            print("%s/%s %s" % (number, len(errors), command))
            subprocess.Popen(command, cwd=os.path.realpath(os.path.curdir), shell=True).wait()


if __name__ == '__main__':
    main()
