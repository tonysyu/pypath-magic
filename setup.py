#! /usr/bin/env python
import setuptools


VERSION = '0.1dev'


with open('README.rst') as f:
    long_description = f.read()


setup_kwargs = {
    'name': 'pypath_magic',
    'description': "Python magic to manipulate the Python path",
    'long_description': long_description,
    'author': 'Tony S. Yu',
    'author_email': 'tsyu80@gmail.com',
    'version': VERSION,
    'license': 'Modified BSD',
    'url': 'http://tonysyu.github.com/pypath_magic',
    'classifiers': [
        'Intended Audience :: Developers',
    ],
    'data_files': [('', ['LICENSE', 'README.rst']),],
    'install_requires': ['IPython >= 1.0'],
}


if __name__ == '__main__':
    setuptools.setup(**setup_kwargs)
