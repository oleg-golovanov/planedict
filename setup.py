from os.path import join, dirname

from setuptools import setup

from planedict import __version__


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
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    test_suite='tests.tests',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
