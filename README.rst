============
pypath-magic
============


``pypath-magic`` adds an `IPython magic`_ (err... Jupyter_ magic?) command for
easily manipulating your Python path. To use the magic command, just load the
extension from an IPython session::

   In [1]: %load_ext pypath_magic

After loading, you will have access to the ``%pypath`` magic. You can type::

   In [2]: %pypath

to list all the custom paths added by ``pypath-magic``. When you get started,
you won't have anything there. To add some custom paths, just change to
a directory and call ``%pypath -a``::

   In [3]: %cd path/to/my-repo

   In [4]: ls
   data_wranglers.py
   plot_helpers.py

   In [5]: %pypath -a
   Added u'/absolute/path/to/my-repo' to path.

   In [6]: %pypath
   /absolute/path/to/my-repo

Now you can reuse those helper functions::

   In [7]: from plot_helpers import plot_slope_marker

Changes to your python path will persist across IPython sessions, and those
paths will be available outside of IPython. If you later want to delete
a directory from your path, just use ``%pypath -d``::

   In [8]: %cd path/to/my-repo

   In [9]: %pypath -d
   Deleted u'/absolute/path/to/my-repo' to path.

You can also list your entire python path with ``%pypath -l``::

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

For additional usage information, type::

   In [11]: %pypath?


Install
=======

To install using pip::

   $ pip install git+https://github.com/tonysyu/pypath-magic

To install from source::

   $ git clone https://github.com/tonysyu/pypath-magic.git
   $ cd pypath-magic
   $ python setup.py install


Dependencies
============

* Python 2.7
* IPython


License
=======

New BSD (a.k.a. Modified BSD). See `LICENSE` in this directory for details.


.. _IPython magic:
   http://ipython.org/ipython-doc/dev/interactive/tutorial.html#magic-functions
.. _Jupyter: http://jupyter.org/