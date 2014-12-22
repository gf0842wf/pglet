# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pglet

setup(name='pglet',
      version='0.0.1',
      description='Fast and simple WSGI-framework for small web-applications.',
      long_description='gevent multi process & multi greenlet',
      author='fk',
      author_email='marc@gsites.de',
      url='https://github.com/gf0842wf/pglet',
      py_modules=['pglet'],
      scripts=['pglet.py'],
      license='MIT',
      platforms = '*nix',
      classifiers=['Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
     )
