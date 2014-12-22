# -*- coding: utf-8 -*-

from distutils.core import setup
import os.path
import sys

import pglet


classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT",
    "Operating System :: *nix",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]


def read(fname):
    fname = os.path.join(os.path.dirname(__file__), fname)
    if sys.version > '3.0':
        content = open(fname, encoding='utf-8').read()
    else:
        content = open(fname).read().decode('utf-8')
    return content.strip()

def read_files(*fnames):
    return '\r\n\r\n\r\n'.join(map(read, fnames))

setup(
    name = 'pglet',
    version='0.0.1',
    packages = [
        #'pglet',
        ],
    description = 'gevent multi process & multi greenlet',
    long_description = read_files('README.md', ),
    license = 'MIT',
    author = 'gf0842wf',
    author_email = 'gf0842wf@gmail.com',
    url = 'https://github.com/gf0842wf/pglet',
    keywords = ['python', 'gevent', 'multiprocessing'],
    classifiers = classifiers, 
    )