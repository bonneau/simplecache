from setuptools import setup

setup(
    name='SimpleCache',
    version='0.1.2',
    author='Scott Bonneau',
    author_email='scott.bonneau@gmail.com',
    packages=['simplecache'],
    scripts=[],
    url='http://pypi.python.org/pypi/SimpleCache/',
    license='LICENSE.txt',
    description='A simple time- and size-based in-memory cache, both threadsafe and non-threadsafe.',
    long_description=open('README.txt').read(),
    install_requires=[],
)