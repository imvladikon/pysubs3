#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
import os
from pathlib import Path

import setuptools

HERE = Path(__file__).parent

__package_name__ = 'pysubs3'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def import_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_version(package_name):
    version = import_file('version',
                          os.path.join(__location__, package_name, 'version.py'))
    return version.__version__


__version__ = get_version(__package_name__)


def read_requirements(reqs_path):
    with open(reqs_path, encoding='utf8') as f:
        reqs = [line.strip() for line in f
                if not line.strip().startswith('#') and not line.strip().startswith('--')]
    return reqs


def get_extra_requires(path, add_all=True, ext='*.txt'):
    main_reqs = read_requirements(HERE / 'requirements.txt')

    extra_deps = {}
    for filename in path.glob(ext):
        # convention of naming requirements files: requirements-{module}.txt
        if not filename.stem.startswith('requirements') or filename.stem == 'requirements':
            continue

        _, _, package_suffix = filename.stem.partition('-')
        reqs = list({*main_reqs, *read_requirements(filename)})
        extra_deps[package_suffix] = reqs

    if add_all:
        extra_deps['all'] = set(vv for v in extra_deps.values() for vv in v)
    return extra_deps


if __name__ == '__main__':
    setuptools.setup(name=__package_name__,
                     version=__version__,
                     author='Vladimir Gurevich',
                     description='pysubs3 (based on pysubs2) is a library for reading subtitle files.',
                     long_description=(HERE / 'README.md').read_text(),
                     long_description_content_type='text/markdown',
                     url='https://github.com/imvladikon/pysubs3',
                     packages=setuptools.find_packages(exclude=(
                         'tests',
                         'tests.*',
                     )),
                     classifiers=[
                         'Programming Language :: Python :: 3',
                         'Topic :: Scientific/Engineering'
                     ],
                     python_requires='>=3.8',
                     package_dir={__package_name__: __package_name__},
                     package_data={
                         __package_name__: ['lang_detector/*.*'],
                     },
                     include_package_data=True,
                     install_requires=read_requirements(HERE / 'requirements.txt'),
                     extras_require=get_extra_requires(HERE))
