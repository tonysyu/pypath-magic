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


def touch_file(path):
    with open(path, 'w'):  # Write empty file.
        pass


def join_with_site_packages_dir(filename):
    return os.path.join(get_python_lib(), filename)


@magics_class
class PathMagic(Magics):

    def __init__(self, *args, **kwargs):
        super(PathMagic, self).__init__(*args, **kwargs)
        filename = os.environ.get('PYPATH_FILENAME', 'pypath_magic.pth')
        self.path_file = join_with_site_packages_dir(filename)

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

        action = None if len(opts) == 0 else opts.keys()[0]

        if action == 'l':
            self.write_lines(sys.path)
            return
        elif action == 'p':
            self.write(self.path_file)
            return

        current_dir = os.getcwdu()

        with open(self.path_file, 'r') as f:
            user_paths = f.readlines()
        user_paths = [p.strip() for p in user_paths if p.strip()]

        if action is None:
            self.write_lines(user_paths)

        elif action == 'a':  # Append current directory to user path.

            if current_dir in user_paths:
                msg = "{!r} is already in the user path."
                self.write(msg.format(current_dir))
                return

            # Add to list for later saving and sys.path for now.
            user_paths.append(current_dir)
            # XXX: This doesn't add to the correct position in sys.path.
            sys.path.append(current_dir)

        elif action == 'd':  # Delete current directory from user path.

            if not current_dir in user_paths:
                msg = "{!r} is not in the user path. Cannot delete."
                self.write(msg.format(current_dir))
                return

            # Remove from list for later saving and sys.path for now.
            user_paths.remove(current_dir)
            sys.path.remove(current_dir)

        if action == 'a' or action == 'd':
            with open(self.path_file, 'w') as f:
                f.write('\n'.join(user_paths))
            if action == 'a':
                self.write('Added {!r} to path.'.format(current_dir))
            else:
                self.write('Deleted {!r} from path'.format(current_dir))

    def write(self, line):
        print(line)

    def write_lines(self, alist):
        self.write('\n'.join(alist))


def load_ipython_extension(ipython):
    ipython.register_magics(PathMagic)
