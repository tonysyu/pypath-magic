import os
from contextlib import contextmanager

from nose.tools import assert_equal

from pypath_magic.core import (PyPath, get_current_directory,
                               join_with_site_packages_dir)


MOCK_PATH_FILE = '_pypath_test_path_.pth'


class TestablePyPath(PyPath):

    def __init__(self, *args, **kwargs):
        super(TestablePyPath, self).__init__(*args, **kwargs)
        self.path_file = join_with_site_packages_dir(MOCK_PATH_FILE)
        self.output = []

    def assert_paths_match(self, paths):
        absolute_paths = [os.path.abspath(p) for p in paths]
        assert_equal(self.current_custom_paths, absolute_paths)

    @property
    def current_custom_paths(self):
        return self._load_user_paths()

    @property
    def output_buffer(self):
        return '\n'.join(self.output)

    def _print(self, line):
        """Override write method to save lines instead of printing."""
        self.output.append(line)

    def _print_empty_list_message(self):
        self._print('')


def touch_file(path):
    with open(path, 'w'):  # Write empty file.
        pass


@contextmanager
def cd(path):
    """Temporarily change directory."""
    original_path = get_current_directory()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_path)


@contextmanager
def make_temp_dirs(paths):
    """Temporarily add directory."""
    # Copy list to ensure that modifications don't affect removal
    paths = list(paths)
    for p in paths:
        os.makedirs(p)
    try:
        yield
    finally:
        for p in paths:
            if os.path.isdir(p):
                os.removedirs(p)


@contextmanager
def cd_temp_directory(path):
    with make_temp_dirs([path]):
        with cd(path):
            yield


@contextmanager
def pypath_test_environment(user_paths=()):
    user_paths = list(user_paths)
    pypath = TestablePyPath()
    if not os.path.exists(pypath.path_file):
        touch_file(pypath.path_file)
    try:
        with make_temp_dirs(user_paths):
            for p in user_paths:
                pypath.add_path(p)
            yield pypath
    finally:
        if os.path.isfile(pypath.path_file):
            os.remove(pypath.path_file)
