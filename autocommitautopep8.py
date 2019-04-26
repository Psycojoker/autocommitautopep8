# encoding: utf-8

import os
import sys
import autopep8
import argparse
import subprocess

from collections import OrderedDict

if sys.version_info[0] == '3':
    unicode = str

errors = OrderedDict([
    ("E101", "Reindent all lines"),
    ("E11", "Fix indentation"),
    ("E121", "Fix indentation to be a multiple of four"),
    # this one seems to be breaking code for some reason :c
    # ("E122", "Add absent indentation for hanging indentation"),
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


def detect_vcs(pwd):
    while pwd != "/" or pwd != os.path.split(pwd)[0]:
        dirs = os.listdir(pwd)

        if ".hg" in dirs:
            print("Info: detecting mercurial cvs")
            return "hg", pwd
        elif ".git" in dirs:
            print("Info: detecting git cvs")
            return "git", pwd

        pwd = os.path.split(pwd)[0]

    raise Exception("Couldn't find which vcs is used :(")


def get_python_files(vcs, path):
    python_files = []

    # git ls-files

    if vcs == "hg":
        all_hg_files = subprocess.check_output(
            "hg status -A", shell=True, cwd=path).decode().split("\n")
        tracked_files = [x.split(" ", 1)[1] for x in all_hg_files if x.startswith("C ")]
    elif vcs == "git":
        tracked_files = subprocess.check_output(
            "git ls-files", shell=True, cwd=path).decode().split("\n")

    tracked_files = filter(None, tracked_files)

    for file in tracked_files:
        file = os.path.join(path, file)
        if file.endswith(".py"):
            python_files.append(file)
        elif os.path.isdir(file):
            continue
        # files without extensions could be python script
        elif "." not in file:
            try:
                is_python_script = "python script" in subprocess.check_output(["file", file]).lower()
            except Exception as e:
                print("Warning: could launch the 'file' command on %s (to check if it's a python script) because of %s" % e)
            else:
                if is_python_script:
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


def fix_files(filenames, options, output=None):
    """Fix list of files."""

    results = []
    current_error = options.select[0] if len(options.select) == 1 else "All"

    for current, name in enumerate(filenames):
        try:
            result = autopep8.fix_file(name, options)
            if result:
                print("\r\033[K%s %s" % (current_error, name))
                results.append(result)
            _display_progess_bar(current, len(filenames), current_error)
        except IOError as error:
            print(unicode(error))

    return results


def _display_progess_bar(current, total, current_error):
    columns = int(subprocess.check_output(
        "stty size", shell=True).decode().split(" ")[1])

    prefix = "%s %s/%s " % (current_error, current, total)

    # " -2" for surrounding "[]"
    inner_bar_length = columns - len(prefix) - 2

    percent = current / float(total)

    current_bar = int(percent * inner_bar_length) * "="

    if current_bar != inner_bar_length and len(current_bar) != 0:
        current_bar = current_bar[:-1] + ">"

    # clear the whole line
    sys.stdout.write("\r\033[K")
    sys.stdout.write("%s[%s%s]\r" % (prefix, current_bar, " " * (inner_bar_length - len(current_bar))))
    sys.stdout.flush()


class FakeOption:
    in_place = True
    line_range = None
    ignore = []
    max_line_length = None
    hang_closing = False
    aggressive = False
    verbose = False
    pep8_passes = -1
    experimental = False
    diff = False
    indent_size = 4
    jobs = 1
    recursive = False
    exclude = None
    max_line_length = 80


def main():
    parser = argparse.ArgumentParser(description='Autocommit autopep8 modifications.')
    parser.add_argument('-s', '--single-commit', action="store_true", default=False, help='do a single commit')
    parser.add_argument('-p', '--path', default=".", help='path to the repository')

    args = parser.parse_args()

    path = os.path.realpath(os.path.expanduser(args.path))

    vcs, vcs_path = detect_vcs(path)

    if vcs == "hg":
        prefix = "hg commit -m"
    elif vcs == "git":
        prefix = "git commit -a -m"
    else:
        raise Exception("Uknown vcs: %s" % vcs)

    python_files = get_python_files(vcs, path=vcs_path)

    options = FakeOption()

    if not args.single_commit:
        for number, (error, description) in enumerate(errors.items(), start=1):
            options.select = [error]
            if fix_files(python_files, options=options):
                command = "{prefix} '[autopep8] {error} - {description}'".format(prefix=prefix, error=error, description=description)
                print("\r\033[K%s/%s %s" % (number, len(errors), command))
                subprocess.Popen(command, cwd=path, shell=True).wait()
    else:
        options.select = errors.keys()
        if fix_files(python_files, options=options):
            command = "{prefix} '[autopep8]'".format(prefix=prefix)
            print("\n%s" % command)
            subprocess.Popen(command, cwd=path, shell=True).wait()


if __name__ == '__main__':
    main()
