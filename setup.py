#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pglet

setup(
      name='pglet',
      version='0.0.1',
      description='gevent multi process & multi greenlet',
      author='fk',
      author_email='gf0842wf@gmail.com',
      url='https://github.com/gf0842wf/pglet',
      packages=['pglet',],
      package_data={'': ['README.md']},
      license='MIT',
      platforms = '*nix',
      classifiers=[
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   ],
      test_suite = 'tests',
     )
