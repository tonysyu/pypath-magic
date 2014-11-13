"""
Core PyPath functionality.

"""
from __future__ import print_function

import os
import sys
from distutils.sysconfig import get_python_lib


def get_current_directory():
    # When requirement is bumped up to IPython >= 2.0, use
    # from IPython.utils.py3compat import getcwd
    try:
        return os.getcwdu()
    except:
        return os.getcwd()


def join_with_site_packages_dir(filename):
    return os.path.join(get_python_lib(), filename)


def save_lines(filename, lines):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))


def is_integer(s):
    try:
        return int(s) == float(s)
    except ValueError:
        return False


class PyPath(object):

    def __init__(self, *args, **kwargs):
        super(PyPath, self).__init__(*args, **kwargs)

        filename = os.environ.get('PYPATH_FILENAME', 'pypath_magic.pth')
        self.path_file = join_with_site_packages_dir(filename)

    # -------------------------------------------------------------------------
    #  Public interface
    # -------------------------------------------------------------------------

    def add_path(self, user_paths, path=None):
        path = path or get_current_directory()
        path = os.path.abspath(path)
        if path in user_paths:
            self._error("{!r} is already in the user path.".format(path))
        elif not os.path.isdir(path):
            self._error("{!r} does not exist.".format(path))

        self._add_path(path, user_paths)
        save_lines(self.path_file, user_paths)
        self._print('Added {!r} to path.'.format(path))

    def delete_path(self, user_paths, path):
        path = self._parse_path_argument(user_paths, path)
        path = os.path.abspath(path)
        if path not in user_paths:
            msg = "{!r} is not in the user path. Cannot delete."
            self._error(msg.format(path))

        self._delete_path(path, user_paths)
        save_lines(self.path_file, user_paths)
        self._print('Deleted {!r} from path'.format(path))

    def list_all_paths(self, user_paths, command_line_args):
        self._print_lines(sys.path)

    def list_custom_paths(self, user_paths, command_line_args):
        self._print_lines([self._numbered_format(index=i, path=path)
                          for i, path in enumerate(user_paths)])

    def print_path_file(self, user_paths, command_line_args):
        self._print(self.path_file)

    def load_user_paths(self):
        with open(self.path_file, 'r') as f:
            user_paths = f.readlines()
        return [p.strip() for p in user_paths if p.strip()]

    # -------------------------------------------------------------------------
    #  Private interface
    # -------------------------------------------------------------------------

    def _print(self, line):
        print(line)

    def _print_lines(self, lines):
        self._print('\n'.join(lines))

    def _error(self, message):
        raise RuntimeError(message)

    def _numbered_format(self, **kwargs):
        return '{index}. {path}'.format(**kwargs)

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