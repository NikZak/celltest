#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
  with io.open(
      join(dirname(__file__), *names), encoding=kwargs.get('encoding',
                                                           'utf8')) as fh:
    return fh.read()


setup(
    name='celltest',
    version='0.0.2',
    license='MIT',
    description='Convert notebook cells to unittests',
    long_description='%s\n%s' %
    (re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
        '', read('README.rst')),
     re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='Nikolay Zakirov',
    author_email='nickzakirov@gmail.com',
    url='https://github.com/NikZak/celltest',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://celltest.readthedocs.io/',
        'Changelog': 'https://celltest.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/NikZak/celltest/issues',
    },
    keywords=[
        'notebook', 'test', 'testing', 'unittest', 'jupyter', 'pytest',
        'coverage'
    ],
    python_requires='>=3.7',
    install_requires=[
        "ipython",
        "nbformat",
        "requests",  # only used in one feature
        "ipykernel",  # only used in one feature
        "notebook",  # only used in one feature
        "pandas"  # only used in examples
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        'black': ['black'],
        'yapf': ['yapf'],
        'isort': ['isort'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={'console_scripts': ['celltest = celltest.cli:main',]},
)
