"""
Core PyPath functionality.

"""
from __future__ import print_function

import os
import sys

from .utils import (get_current_directory, is_integer,
                    join_with_site_packages_dir, save_lines, touch_file)


ACTION_DOCSTRINGS = {
    'list': "List all paths defined by user.",
    'add': "Add path to user's Python path.",
    'delete': "Delete path from user's Python path.",
    'list_all': "List all paths in user's Python path.",
    'path_file': "Print path to user's path file.",
}


class PyPath(object):

    def __init__(self, *args, **kwargs):
        # Default pypath filename can be overridden by environment variable
        # or keyword argument---in that order.
        filename = os.environ.get('PYPATH_FILENAME', 'pypath_magic.pth')
        filename = kwargs.get('pypath_filename', filename)
        self.path_file = join_with_site_packages_dir(filename)

        if not os.path.isfile(self.path_file):
            touch_file(self.path_file)

        self._help_command = 'pypath -h'

    # -------------------------------------------------------------------------
    #  Public interface
    # -------------------------------------------------------------------------

    def add_path(self, path=None):
        user_paths = self._load_user_paths()
        path = path or get_current_directory()
        path = os.path.abspath(path)
        if path in user_paths:
            self._error("{!r} is already in the user path.".format(path))
        elif not os.path.isdir(path):
            self._error("{!r} does not exist.".format(path))

        self._add_path(path, user_paths)
        save_lines(self.path_file, user_paths)
        self._print('Added {!r} to path.'.format(path))

    def delete_path(self, path=''):
        user_paths = self._load_user_paths()
        path = self._parse_path_argument(user_paths, path)
        path = os.path.abspath(path)
        if path not in user_paths:
            msg = "{!r} is not in the user path. Cannot delete."
            self._error(msg.format(path))

        self._delete_path(path, user_paths)
        save_lines(self.path_file, user_paths)
        self._print('Deleted {!r} from path'.format(path))

    def list_all_paths(self, _=None):
        self._print_lines(sys.path)

    def list_custom_paths(self, _=None):
        user_paths = self._load_user_paths()
        if user_paths:
            self._print_lines([self._numbered_format(index=i, path=path)
                               for i, path in enumerate(user_paths)])
        else:
            self._print_empty_list_message()

    def print_path_file(self, _=None):
        self._print(self.path_file)

    # -------------------------------------------------------------------------
    #  Private interface
    # -------------------------------------------------------------------------

    def _print(self, line):
        print(line)

    def _print_lines(self, lines):
        self._print('\n'.join(lines))

    def _print_empty_list_message(self):
        msg = ("No user paths are defined.\n"
               "See `{help_command}` for usage information.")
        self._print(msg.format(help_command=self._help_command))

    def _error(self, message):
        raise RuntimeError(message)

    def _numbered_format(self, **kwargs):
        return '{index}. {path}'.format(**kwargs)

    def _load_user_paths(self):
        with open(self.path_file, 'r') as f:
            user_paths = f.readlines()
        return [p.strip() for p in user_paths if p.strip()]

    @staticmethod
    def _add_path(path, user_paths):
        """Add to list for later saving and sys.path for now."""
        user_paths.append(path)

    @staticmethod
    def _delete_path(path, user_paths):
        """Delete from list for later saving and sys.path for now."""
        user_paths.remove(path)

    def _parse_path_argument(self, user_paths, path_arg):
        """Return path from input argument.

        Possible `path_arg` values:

            empty:
                Use current directory.
            integer:
                Index into current list of custom user paths.
            string:
                A string representing the system path.
        """
        if is_integer(path_arg):
            index = int(path_arg)
            if index >= len(user_paths):
                msg = "Index {} exceeds the number of known user paths."
                self._error(msg.format(index))
            return user_paths[index]
        elif len(path_arg):
            return path_arg
        else:
            return get_current_directory()
