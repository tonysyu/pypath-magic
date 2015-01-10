import os
from distutils.sysconfig import get_python_lib


def touch_file(path):
    with open(path, 'w'):  # Write empty file.
        pass


def get_current_directory():
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
