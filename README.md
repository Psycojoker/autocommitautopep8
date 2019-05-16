AutoCommitAutoPEP8
==================

autocommitautopep8 is a script that will run autopep8 on all the tracked python
files of your hg/git project and generate one commit per PEP8 error it fixes
(or a single one if you want.)

The idea is to automate the job you don't care about.

Installation
------------

    pip install --user autocommitautopep8

Usage
-----

Launch this in your hg/git repository:

    autocommitautopep8

This will ask hg/git all the files it is tracking and will apply autopep8 on it
error category by error category and will do one commit per error category if
some thing have been fixed.

Be aware that this can take quite some time but at least you have a nice
progress bar.

If you wish to do a single commit instead, you can use the
"-s"/"--single-commit" option:

    autocommitautopep8 -s

You can also specify a path to your repository using "-p"/"--path" (but be
aware that this will still use hg/git to get a list of the tracked files):

    autocommitautopep8 --path path/to/my/project

Note that this will also work as autocommitautopep8 will go up in the
hierarchy path until it finds a ".hg" or a ".git".

    autocommitautopep8 --path path/to/my/project/subdir

If needed, you can restrict the files on which you want to apply
autocommitautopep8 using the "-f"/"--files" argument:

    autocommitautopep8 -f file1 file2 file3

Not that this will match all files contains in the dvcs which path ends with
one of the filename/path/partial path specified.
