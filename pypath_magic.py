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
from distutils.sysconfig import get_python_lib

from IPython.core.error import UsageError
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.utils.py3compat import getcwd


def join_with_site_packages_dir(filename):
    return os.path.join(get_python_lib(), filename)


def save_lines(filename, lines):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))


def touch_file(path):
    with open(path, 'w'):  # Write empty file.
        pass


def is_integer(s):
    try:
        return int(s) == float(s)
    except ValueError:
        return False


@magics_class
class PathMagic(Magics):

    def __init__(self, *args, **kwargs):
        super(PathMagic, self).__init__(*args, **kwargs)

        filename = os.environ.get('PYPATH_FILENAME', 'pypath_magic.pth')
        self.path_file = join_with_site_packages_dir(filename)

        self._action_calls = {'': self._do_list_custom_paths,
                              'a': self._do_add_path,
                              'd': self._do_delete_path,
                              'l': self._do_list_all_paths,
                              'p': self._do_print_path_file}

    #--------------------------------------------------------------------------
    #  Public interface
    #--------------------------------------------------------------------------

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
        if not os.path.isfile(self.path_file):
            touch_file(self.path_file)

        opts, command_line_args = self.parse_options(line, 'adlp')
        if len(opts) > 1:
            self._error("%pypath: Only a single option allowed.")

        action = '' if len(opts) == 0 else list(opts.keys())[0]

        if action not in 'ad' and command_line_args:
            msg = "No arguments allowed for '%pypath -{}'."
            raise UsageError(msg.format(action))

        user_paths = self._load_user_paths()
        self._action_calls[action](user_paths, command_line_args)

    #--------------------------------------------------------------------------
    #  Action interface
    #--------------------------------------------------------------------------

    def _do_add_path(self, user_paths, command_line_args):
        path = command_line_args or getcwd()
        path = os.path.abspath(path)
        if path in user_paths:
            self._error("{!r} is already in the user path.".format(path))
        elif not os.path.isdir(path):
            self._error("{!r} does not exist.".format(path))

        self._add_path(path, user_paths)
        save_lines(self.path_file, user_paths)
        self._print('Added {!r} to path.'.format(path))

    def _do_delete_path(self, user_paths, command_line_args):
        path = self._parse_path_argument(user_paths, command_line_args)
        path = os.path.abspath(path)
        if not path in user_paths:
            msg = "{!r} is not in the user path. Cannot delete."
            self._error(msg.format(path))

        self._delete_path(path, user_paths)
        save_lines(self.path_file, user_paths)
        self._print('Deleted {!r} from path'.format(path))

    def _do_list_all_paths(self, user_paths, command_line_args):
        self._print_lines(sys.path)

    def _do_list_custom_paths(self, user_paths, command_line_args):
        self._print_lines([self._numbered_format(index=i, path=path)
                          for i, path in enumerate(user_paths)])

    def _do_print_path_file(self, user_paths, command_line_args):
        self._print(self.path_file)

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _print(self, line):
        print(line)

    def _print_lines(self, lines):
        self._print('\n'.join(lines))

    def _error(self, message):
        raise UsageError(message)

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
        # XXX: This doesn't add to the correct position in sys.path.
        sys.path.append(path)

    @staticmethod
    def _delete_path(path, user_paths):
        """Delete from list for later saving and sys.path for now."""
        user_paths.remove(path)
        sys.path.remove(path)

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
            return getcwd()


def load_ipython_extension(ipython):
    ipython.register_magics(PathMagic)
