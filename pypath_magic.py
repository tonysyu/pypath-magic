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


def get_current_directory():
    return os.getcwdu()


def join_with_site_packages_dir(filename):
    return os.path.join(get_python_lib(), filename)


def save_lines(filename, lines):
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))


def touch_file(path):
    with open(path, 'w'):  # Write empty file.
        pass


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

        opts, args = self.parse_options(line, 'adlp')
        if args:
            raise UsageError("%pypath: No arguments allowed.")
        if len(opts) > 1:
            raise UsageError("%pypath: Only a single option allowed.")

        action = '' if len(opts) == 0 else opts.keys()[0]

        user_paths = self._load_user_paths()
        return self._action_calls[action](user_paths)

    def write(self, line):
        print(line)

    def write_lines(self, lines):
        self.write('\n'.join(lines))

    #--------------------------------------------------------------------------
    #  Action interface
    #--------------------------------------------------------------------------

    def _do_add_path(self, user_paths):
        current_dir = get_current_directory()
        if current_dir in user_paths:
            msg = "{!r} is already in the user path."
            self.write(msg.format(current_dir))
            return

        self._add_path(current_dir, user_paths)
        save_lines(self.path_file, user_paths)
        self.write('Added {!r} to path.'.format(current_dir))

    def _do_delete_path(self, user_paths):
        current_dir = get_current_directory()
        if not current_dir in user_paths:
            msg = "{!r} is not in the user path. Cannot delete."
            self.write(msg.format(current_dir))
            return

        self._delete_path(current_dir, user_paths)
        save_lines(self.path_file, user_paths)
        self.write('Deleted {!r} from path'.format(current_dir))

    def _do_list_all_paths(self, user_paths):
        self.write_lines(sys.path)

    def _do_list_custom_paths(self, user_paths):
        self.write_lines(self._load_user_paths())

    def _do_print_path_file(self, user_paths):
        self.write(self.path_file)

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

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


def load_ipython_extension(ipython):
    ipython.register_magics(PathMagic)
