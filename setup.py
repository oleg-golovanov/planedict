from setuptools import setup

from planedict import __version__
from planedict.planedict import __doc__


setup(
    name='planedict',
    version=__version__,
    packages=['planedict'],
    url='https://github.com/oleg-golovanov/planedict',
    license='MIT',
    author='Oleg Golovanov',
    author_email='golovanov.ov@gmail.com',
    description='PlaneDict is a dict-like class which represents built-in dict class '
                'as a \'plane\' structure, i.e. pairs path-value. Path is a tuple of keys, '
                'value is value which allows in built-in dict.',
    zip_safe=False,
    platforms='any',
    long_description=__doc__,
    test_suite='tests.tests'
)
