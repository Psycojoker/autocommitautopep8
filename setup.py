#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

setup(name='autocommitautopep8',
      version='0.2',
      description='auto generate git/hg commits per autopep8 fixes',
      author='Laurent Peuch',
      # long_description='',
      author_email='cortex@worlddomination.be',
      url='https://github.com/Psycojoker/autocommitautopep8',
      install_requires=['autopep8'],
      py_modules=['autocommitautopep8'],
      license='gplv3+',
      entry_points={
          'console_scripts': [
              'autocommitautopep8 = autocommitautopep8:main'
          ]
      },
      keywords='pep8 autopep8 formatting',
      )
