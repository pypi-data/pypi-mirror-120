#!/usr/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='connectwrap',
    version='1.1.6',
    packages=find_packages(),
    license='MIT',
    description='Python package made to manage, display & parse data from SQLite file databases.',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/connectwrap-sqlite3',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux'],
    python_requires='>=3.6'
)

# - Update README.md
# - Update Version Number
# - Tar Wrap the Package: python setup.py sdist
# - Check Package: twine check dist/*
# - Upload to PYPI: twine upload dist/*
# - Commit Changes
# - Change Release Version in Github Repo