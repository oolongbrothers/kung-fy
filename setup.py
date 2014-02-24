from setuptools import setup, find_packages
import os
import re
import codecs

# Examples:
#   https://github.com/pypa/sampleproject/blob/master/setup.py
#   http://pythonhosted.org/an_example_pypi_project/setuptools.html#using-setup-py

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    """
    Read the version number from a source file.
    Why read it, and not import?
    see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
    """
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(fname):
    return open(os.path.join(here, fname)).read()


setup(
    name = 'kung-fy',
    version = find_version('kungfy/kungfy.py'),
    author = "Alexander Bethke",
    author_email = "oolongbrothers@gmx.net",
    description = ("Script for nas-based banshee state storage"),
    long_description=read('README'),
    license = "GPLv3",
    url = 'https://github.com/oolongbrothers/kung-fy',
    keywords = 'linux banshee music player playlist synchronisation',
    classifiers = ["Development Status :: 3 - Alpha"],

    packages = ['kungfy'],
    install_requires = ['pyyaml', 'nose'],
    test_suite = 'nose.collector',
    scripts = ["bin/kung-fy"]
)
