from setuptools import setup, find_packages

# Example: https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name = 'kung-fy',
    version = '0.5.0',
    install_requires = ['pyyaml', 'nose'],
    packages=['kungfy'],
    test_suite = 'nose.collector'
)
