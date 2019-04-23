AutoCommitAutoPEP8
==================

autocommitautopep8 is a script that will run autopep8 on all the tracked python
files of your hg/git project and generate one commit per PEP8 error it fixes
(or a single one if you want.)

The idea is to automate the job you don't care about.

Installation
------------

    pip install --user git+https://github.com/Psycojoker/autocommitautopep8

Usage
-----

Launch this in your hg/git repository:

    autocommitautopep8

This will ask hg/git all the files it is tracking and will apply autopep8 on it
error category by error category and will do one commit per error category if
some thing have been fixed.

Be aware that this can take quite some time but at least you have a nice
progress bar.

If you which to do a signe commit instead, you can use the
"-s"/"--single-commit" option:

    autocommitautopep8 -s
