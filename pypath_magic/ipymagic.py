"""
IPython extension for managing the Python path.

    %load_ext pypath_magic

After loading, you will have access to the `%pypath` magic. For usage
information, type

    %pypath?

"""
from __future__ import print_function

import os
import sys

from IPython.core.error import UsageError
from IPython.core.magic import Magics, magics_class, line_magic

from .core import PyPath


def touch_file(path):
    with open(path, 'w'):  # Write empty file.
        pass


class IPyPath(PyPath):

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
        super(PathMagic, self).__init__(*args, **kwargs)

        self._pypath_cmd = IPyPath()
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
        """Manage user's Python path.

        %pypath              - List all paths defined by user.
        %pypath -a           - Add current path to user path.
        %pypath -d           - Delete current path from user path.
        %pypath -l           - List all paths (including pre-defined paths).
        %pypath -p           - Print path to user's path file.

        The added paths persist through sessions and are stored separately
        from paths added by setuptools/pip (see `%pypath -p`).
        """
        if not os.path.isfile(self._pypath_cmd.path_file):
            touch_file(self._pypath_cmd.path_file)

        opts, command_line_args = self.parse_options(line, 'adlp')
        if len(opts) > 1:
            self._error("%pypath: Only a single option allowed.")

        action = '' if len(opts) == 0 else list(opts.keys())[0]

        if action not in 'ad' and command_line_args:
            msg = "No arguments allowed for '%pypath -{}'."
            raise UsageError(msg.format(action))

        user_paths = self._pypath_cmd.load_user_paths()
        self._action_calls[action](user_paths, command_line_args)

    # -------------------------------------------------------------------------
    #  Action interface
    # -------------------------------------------------------------------------

    def _do_add_path(self, user_paths, command_line_args):
        self._pypath_cmd.add_path(user_paths, command_line_args)

    def _do_delete_path(self, user_paths, command_line_args):
        self._pypath_cmd.delete_path(user_paths, command_line_args)

    def _do_list_all_paths(self, user_paths, command_line_args):
        self._pypath_cmd.list_all_paths(user_paths, command_line_args)

    def _do_list_custom_paths(self, user_paths, command_line_args):
        self._pypath_cmd.list_custom_paths(user_paths, command_line_args)

    def _do_print_path_file(self, user_paths, command_line_args):
        self._pypath_cmd.print_path_file(user_paths, command_line_args)

    # -------------------------------------------------------------------------
    #  Private interface
    # -------------------------------------------------------------------------


def load_ipython_extension(ipython):
    ipython.register_magics(PathMagic)
