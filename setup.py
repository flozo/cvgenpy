#!/usr/bin/env python3
"""
Setup module for cvgen
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Use README.md file as long description
long_description = (here/'README.md').read_text(encoding='utf-8')

setup(
        name = 'cvgen',
        version = '0.21',
        description = 'A program for generating a curriculum vitae.',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
#        url = 'https://github.com/flozo/Reponame',
        author = 'Johannes Engelmayer',
#        author_email = 'mail@mail.net',
# Classifiers from https://pypi.org/classifiers/
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Natural Language :: German',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Topic :: Office/Business',
            'Topic :: Text Processing',
            'Topic :: Text Processing :: Markup',
            'Topic :: Text Processing :: Markup :: LaTeX',
            ],
        keywords = 'curriculum vitae, LaTeX, markup',
        package_dir = {'':'src'},
        packages = find_packages(where='src'),
        install_requires = ['argparse'],
    )

