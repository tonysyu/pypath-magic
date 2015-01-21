#! /usr/bin/env python
import setuptools


VERSION = '0.3.0'


with open('README.rst') as f:
    long_description = f.read()


setup_kwargs = {
    'name': 'pypath_magic',
    'description': "IPython magic and CLI to manipulate the Python path",
    'long_description': long_description,
    'author': 'Tony S. Yu',
    'author_email': 'tsyu80@gmail.com',
    'py_modules': ['pypath_magic'],
    'version': VERSION,
    'license': 'Modified BSD',
    'url': 'http://tonysyu.github.com/pypath_magic',
    'download_url': 'http://tonysyu.github.com/pypath_magic',
    'classifiers': [
        'Topic :: Utilities',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Topic :: Desktop Environment :: File Managers',
    ],
    'keywords': ['PYTHONPATH', 'utility', 'IPython'],
    'install_requires': ['IPython >= 1.0'],
    'entry_points': {'console_scripts': ['pypath = pypath_magic.cli:main']},
}


if __name__ == '__main__':
    setuptools.setup(**setup_kwargs)
