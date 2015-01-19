import os
import sys
from contextlib import contextmanager

from nose.tools import assert_equal, assert_raises, raises

from .core import PyPath
from .utils import get_current_directory


MOCK_PATH_FILE = '_pypath_test_path_.pth'


class TestablePyPath(PyPath):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('pypath_filename', MOCK_PATH_FILE)
        super(TestablePyPath, self).__init__(*args, **kwargs)
        self.output = []

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


def assert_paths_match(pypath, paths):
    absolute_paths = [os.path.abspath(p) for p in paths]
    assert_equal(pypath.current_custom_paths, absolute_paths)


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


# -------------------------------------------------------------------------
#  Test runners
# -------------------------------------------------------------------------


class BasicPyPathInterface(object):

    def test_empty(self):
        self.pypath.list_custom_paths()
        assert_equal(self.pypath.output_buffer, '')

    def test_list_all_paths(self):
        self.pypath.list_all_paths()
        expected_paths = set(p for p in sys.path if len(p))
        result = set(p for p in self.pypath.output_buffer.split() if len(p))
        assert_equal(result, expected_paths)

    def test_print_pypath_file_path(self):
        self.pypath.print_path_file()
        assert self.pypath.output[-1].endswith(MOCK_PATH_FILE)

    def test_add_current_directory(self):
        with cd_temp_directory('_dummy_'):
            self.pypath.add_path()
            assert_paths_match(self.pypath, [get_current_directory()])

    def test_add_and_remove(self):
        with cd_temp_directory('_dummy_'):
            self.pypath.add_path()
            self.pypath.delete_path()
            assert_equal(len(self.pypath.current_custom_paths), 0)


class PyPathAddInterface(object):

    error_class = RuntimeError

    def test_add_multiple_directories(self):
        self.pypath.add_path()
        with cd_temp_directory('_dummy_'):
            self.pypath.add_path()
        assert_equal(len(self.pypath.current_custom_paths), 2)
        assert_paths_match(self.pypath, ['.', '_dummy_'])

    def test_add_absolute_path_input(self):
        current_directory = get_current_directory()
        self.pypath.add_path(current_directory)
        assert_paths_match(self.pypath, [current_directory])

    def test_add_relative_path_input(self):
        with make_temp_dirs(['./_dummy_']):
            self.pypath.add_path('_dummy_')
            assert_paths_match(self.pypath, ['_dummy_'])

    def test_add_nonexistent_path(self):
        with assert_raises(self.error_class):
            self.pypath.add_path('path/that/does/not/exist')


class PyPathDeleteInterface(object):

    error_class = RuntimeError

    def init_user_paths(self, user_paths):
        with make_temp_dirs(user_paths):
            for p in user_paths:
                self.pypath.add_path(p)

    def test_delete_index(self):
        user_paths = ['a/b/c', 'd/e/f', 'g/h', 'i/j']
        self.init_user_paths(user_paths)

        self.pypath.delete_path('1')
        user_paths.pop(1)
        assert_paths_match(self.pypath, user_paths)

    def test_delete_relative_path(self):
        user_paths = ['a/b/c', 'd/e/f', 'g/h', 'i/j']
        self.init_user_paths(user_paths)

        self.pypath.delete_path('d/e/f')
        user_paths.pop(1)
        assert_paths_match(self.pypath, user_paths)

    def test_delete_nonexistent_path(self):
        with assert_raises(self.error_class):
            self.pypath.delete_path('path/that/does/not/exist')

    def test_delete_nonexistent_index(self):
        with assert_raises(self.error_class):
            self.pypath.delete_path('1')
