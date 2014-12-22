# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='pglet',
    version='0.0.1',
    description='gevent multi process & multi greenlet',
    long_description=open('README.md').read(),
    author='fk',
    author_email='gf0842wf@gmail.com',
    url='https://github.com/gf0842wf/pglet',
    packages=find_packages(),
    license=open('LICENSE').read(),
    include_package_data=True,
    keywords=['python', 'gevent', 'multiprocessing'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
    install_requires=[
        'gevent',
        'gipc',
    ]
)