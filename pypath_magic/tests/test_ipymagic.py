import os
import sys
from contextlib import contextmanager

from nose.tools import assert_equal, raises
from IPython.core.error import UsageError

from pypath_magic.core import (get_current_directory,
                               join_with_site_packages_dir)
from pypath_magic.ipymagic import IPyPath, PathMagic


# -------------------------------------------------------------------------
#  Test helpers
# -------------------------------------------------------------------------


MOCK_PATH_FILE = '_pypath_test_path_.pth'


class TestablePyPath(IPyPath):

    def __init__(self, *args, **kwargs):
        super(IPyPath, self).__init__(*args, **kwargs)
        self.path_file = join_with_site_packages_dir(MOCK_PATH_FILE)
        self.output = []

    def _print(self, line):
        """Override write method to save lines instead of printing."""
        self.output.append(line)

    def _print_empty_list_message(self):
        self._print('')


class TestablePathMagic(PathMagic):

    def __init__(self, *args, **kwargs):
        super(TestablePathMagic, self).__init__(*args, **kwargs)
        self._pypath_cmd = TestablePyPath()

    def __call__(self, *args, **kwargs):
        self.pypath(*args, **kwargs)

    @property
    def path_file(self):
        return self._pypath_cmd.path_file

    @property
    def output_buffer(self):
        return '\n'.join(self._pypath_cmd.output)

    @property
    def output_lines(self):
        return self.output_buffer.split('\n')

    @property
    def last_output(self):
        return self.output_lines[-1]

    @property
    def current_custom_paths(self):
        self('')  # Calling `pypath` with no arguments lists custom paths.
        lines = self._pypath_cmd.output.pop()
        if len(lines.strip()):
            # One path on each line, a space separates the index from path.
            return [each.split()[1] for each in lines.split('\n')]
        else:
            return []

    def assert_paths_match(self, paths):
        assert_equal(len(self.current_custom_paths), len(paths))
        absolute_paths = [os.path.abspath(p) for p in paths]
        assert_equal(self.current_custom_paths, absolute_paths)


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
    pypath = TestablePathMagic()
    try:
        with make_temp_dirs(user_paths):
            for p in user_paths:
                pypath('-a {}'.format(p))
            yield pypath
    finally:
        if os.path.isfile(pypath.path_file):
            os.remove(pypath.path_file)


# -------------------------------------------------------------------------
#  Tests
# -------------------------------------------------------------------------

def test_empty():
    with pypath_test_environment() as pypath:
        pypath('')
        assert_equal(pypath.output_buffer, '')


def test_list_all_paths():
    with pypath_test_environment() as pypath:
        pypath('-l')
        expected_paths = set(p for p in sys.path if len(p))
        result = set(p for p in pypath.output_buffer.split() if len(p))
        assert_equal(result, expected_paths)


def test_print_pypath_file_path():
    with pypath_test_environment() as pypath:
        pypath('-p')
        print pypath.last_output[-len(MOCK_PATH_FILE):], MOCK_PATH_FILE
        print pypath.last_output, MOCK_PATH_FILE
        assert pypath.last_output.endswith(MOCK_PATH_FILE)


def test_add_current_directory():
    with pypath_test_environment() as pypath:
        pypath('-a')
        pypath.assert_paths_match([get_current_directory()])


def test_add_and_remove():
    with pypath_test_environment() as pypath:
        pypath('-a')
        pypath('-d')
        assert_equal(len(pypath.current_custom_paths), 0)


# -------------------------------------------------------------------------
#  Test `%pypath -a`
# -------------------------------------------------------------------------

def test_add_multiple_directories():
    with pypath_test_environment() as pypath:
        pypath('-a')
        with cd_temp_directory('_dummy_'):
            pypath('-a')
        assert_equal(len(pypath.current_custom_paths), 2)
        pypath.assert_paths_match(['.', '_dummy_'])


def test_add_absolute_path_input():
    with pypath_test_environment() as pypath:
        current_directory = get_current_directory()
        pypath('-a {}'.format(current_directory))
        pypath.assert_paths_match([current_directory])


def test_add_relative_path_input():
    with make_temp_dirs(['./_dummy_']):
        with pypath_test_environment() as pypath:
            pypath('-a {}'.format('_dummy_'))
            pypath.assert_paths_match(['_dummy_'])


@raises(UsageError)
def test_add_nonexistent_path():
    with pypath_test_environment() as pypath:
        pypath('-a path/that/does/not/exist')


# -------------------------------------------------------------------------
#  Test `%pypath -d'
# -------------------------------------------------------------------------

def test_delete_index():
    user_paths = ['a/b/c', 'd/e/f', 'g/h', 'i/j']
    with pypath_test_environment(user_paths=user_paths) as pypath:
        pypath('-d 1')
        user_paths.pop(1)
        pypath.assert_paths_match(user_paths)


def test_delete_relative_path():
    user_paths = ['a/b/c', 'd/e/f', 'g/h', 'i/j']
    with pypath_test_environment(user_paths=user_paths) as pypath:
        pypath('-d d/e/f')
        user_paths.pop(1)
        pypath.assert_paths_match(user_paths)


@raises(UsageError)
def test_delete_nonexistent_path():
    with pypath_test_environment() as pypath:
        pypath('-d path/that/does/not/exist')


@raises(UsageError)
def test_delete_nonexistent_index():
    with pypath_test_environment() as pypath:
        pypath('-d 1')
