============
pypath-magic
============


``pypath-magic`` provides a simple interface for adding modules and packages
to your Python path. This page should provide a good overview, but you might
also want to check out the
`original pypath-magic article <http://tonysyu.github.io/pypath-magic.html>`_
and the
`article introducing the command-line interface <http://tonysyu.github.io/pypath-magic-v03.html>`_

Unlike modifications to ``sys.path``, this allows you to easily modify your
path across sessions. Unlike modifications to environment variables, this
doesn't require you to explain to users, students, and colleagues how to modify
environment variables.


Command-line interface
======================

In addition to the namesake IPython magic interface, version 0.3 adds a
command-line interface (CLI) that resembles the IPython interface. After
installing the latest version (``pip install pypath_magic``), you'll have
access to a ``pypath`` command in your favorite terminal/shell.

An example IPython workflow with ``pypath-magic`` is described below. The CLI
has a similar interface::

   pypath <command> [PATH]

The standard commands are::

   pypath add [PATH]       Add path to user's Python path.
   pypath delete [PATH]    Delete path from user's Python path.
   pypath [list]           List all paths defined by user.
   pypath list-all         List all paths in user's Python path.
   pypath path-file        Print path to user's path file.

Continue below to this in action for the IPython interface.


IPython magic
=============

``pypath-magic`` adds an `IPython magic`_ (err... Jupyter_ magic?) command for
easily manipulating your Python path. To use the magic command, just load the
extension from an IPython session:

.. code-block:: python

   In [1]: %load_ext pypath_magic

After loading, you will have access to the ``%pypath`` magic. You can type:

.. code-block:: python

   In [2]: %pypath

to list all the custom paths added by ``pypath-magic``. When you get started,
you won't have anything there. To add some custom paths, just change to
a directory and call ``%pypath -a``:

.. code-block:: python

   In [3]: %cd path/to/my-repo

   In [4]: ls
   data_wranglers.py
   plot_helpers.py

   In [5]: %pypath -a
   Added u'/absolute/path/to/my-repo' to path.

   In [6]: %pypath
   /absolute/path/to/my-repo

Now you can reuse those helper functions:

.. code-block:: python

   In [7]: from plot_helpers import plot_slope_marker

Changes to your python path will persist across IPython sessions, and those
paths will be available outside of IPython. If you later want to delete
a directory from your path, just use ``%pypath -d``:

.. code-block:: python

   In [8]: %cd path/to/my-repo

   In [9]: %pypath -d
   Deleted u'/absolute/path/to/my-repo' from path.

You can also list your entire python path with ``%pypath -l``:

.. code-block:: python

   In [10]: %pypath -l

   /Users/tonysyu/code/yutils
   /Users/tonysyu/code/skimage
   /Users/tonysyu/code/mpl/lib
   /Users/tonysyu/code/ipython
   /Users/tonysyu/code/deli
   /Users/tonysyu/code/mpltools
   /Applications/Canopy.app/appdata/canopy-1.4.1.1975.macosx-x86_64/Canopy.app/Contents/lib/python27.zip
   /Applications/Canopy.app/appdata/canopy-1.4.1.1975.macosx-x86_64/Canopy.app/Contents/lib/python2.7
   ...
   /absolute/path/to/my-repo

For additional usage information, type:

.. code-block:: python

   In [11]: %pypath?


Install
=======

To install using pip::

   $ pip install pypath_magic

To install from source::

   $ git clone https://github.com/tonysyu/pypath-magic.git
   $ cd pypath-magic
   $ python setup.py install

If you get an error like::

   error: invalid command 'egg_info'

you probably need to update ``setuptools``::

   pip install --upgrade setuptools


Dependencies
============

* Python 2.7/3.4 (older versions probably work, but this is not tested)
* IPython >= 1.1
* setuptools >= 0.7


License
=======

New BSD (a.k.a. Modified BSD). See LICENSE_ file in this directory for details.


.. _IPython magic:
   http://ipython.org/ipython-doc/dev/interactive/tutorial.html#magic-functions
.. _Jupyter: http://jupyter.org/
.. _LICENSE: https://github.com/tonysyu/pypath-magic/blob/master/LICENSE
