"""
IPython extension for managing the Python path.

    %load_ext pypath_magic

After loading, you will have access to the `%pypath` magic. For usage
information, type

    %pypath?

"""
from __future__ import print_function

import sys

from IPython.core.error import UsageError
from IPython.core.magic import Magics, magics_class, line_magic

from .core import ACTION_DOCSTRINGS, PyPath


PYPATH_HELP = """\
PyPath magic for manipulating a user's Python path.

%pypath              - {list}
%pypath -a           - {add}
%pypath -d           - {delete}
%pypath -l           - {list_all}
%pypath -p           - {path_file}

The added paths persist through sessions and are stored separately
from paths added by setuptools/pip (see `%pypath -p`).
""".format(**ACTION_DOCSTRINGS)


class IPyPath(PyPath):

    def __init__(self, *args, **kwargs):
        super(IPyPath, self).__init__(*args, **kwargs)
        self._help_command = '%pypath?'

    @staticmethod
    def _add_path(path, user_paths):
        """Add to list for later saving and sys.path for now."""
        PyPath._add_path(path, user_paths)
        # XXX: This doesn't add to the correct position in sys.path.
        sys.path.append(path)

    def _error(self, message):
        raise UsageError(message)

    @staticmethod
    def _delete_path(path, user_paths):
        """Delete from list for later saving and sys.path for now."""
        PyPath._delete_path(path, user_paths)
        sys.path.remove(path)


@magics_class
class PathMagic(Magics):

    def __init__(self, *args, **kwargs):
        fname = kwargs.pop('pypath_filename', None)
        pypath_kwargs = ({} if fname is None else {'pypath_filename': fname})
        self._pypath_cmd = IPyPath(**pypath_kwargs)

        super(PathMagic, self).__init__(*args, **kwargs)

        self._action_calls = {'': self._do_list_custom_paths,
                              'a': self._do_add_path,
                              'd': self._do_delete_path,
                              'l': self._do_list_all_paths,
                              'p': self._do_print_path_file}

    # -------------------------------------------------------------------------
    #  Public interface
    # -------------------------------------------------------------------------

    @line_magic('pypath')
    def pypath(self, line):
        opts, command_line_args = self.parse_options(line, 'adlp')
        if len(opts) > 1:
            self._error("%pypath: Only a single option allowed.")

        action = '' if len(opts) == 0 else list(opts.keys())[0]

        if action not in 'ad' and command_line_args:
            msg = "No arguments allowed for '%pypath -{}'."
            raise UsageError(msg.format(action))

        self._action_calls[action](command_line_args)

    # Patch docstring since we can't use `str.format` with docstrings.
    pypath.__doc__ = PYPATH_HELP

    # -------------------------------------------------------------------------
    #  Action interface
    # -------------------------------------------------------------------------

    def _do_add_path(self, command_line_args):
        self._pypath_cmd.add_path(command_line_args)

    def _do_delete_path(self, command_line_args):
        self._pypath_cmd.delete_path(command_line_args)

    def _do_list_all_paths(self, command_line_args):
        self._pypath_cmd.list_all_paths()

    def _do_list_custom_paths(self, command_line_args):
        self._pypath_cmd.list_custom_paths()

    def _do_print_path_file(self, command_line_args):
        self._pypath_cmd.print_path_file()

    # -------------------------------------------------------------------------
    #  Private interface
    # -------------------------------------------------------------------------


def load_ipython_extension(ipython):
    ipython.register_magics(PathMagic)
