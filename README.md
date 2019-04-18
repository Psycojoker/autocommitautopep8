AutoCommitAutoPEP8
==================

autocommitautopep8 is a script that will run autopep8 on all the files of your
python project and generate one commit per PEP8 error it fixes.

The idea is to automate the job you don't care about.

Installation
------------

    pip install --user git+https://github.com/Psycojoker/autocommitautopep8

Usage
-----

    autocommitautopep8

This will recursively parse the files and apply itself on Python files.

Be aware that this can take quite some time.
