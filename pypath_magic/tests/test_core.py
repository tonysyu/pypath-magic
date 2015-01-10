import sys

from nose.tools import assert_equal, raises

from pypath_magic.core import get_current_directory
from pypath_magic.testing import (MOCK_PATH_FILE,
                                  cd_temp_directory, make_temp_dirs,
                                  pypath_test_environment)

# -------------------------------------------------------------------------
#  Basic tests
# -------------------------------------------------------------------------

def test_empty():
    with pypath_test_environment() as pypath:
        pypath.list_custom_paths()
        assert_equal(pypath.output_buffer, '')


def test_list_all_paths():
    with pypath_test_environment() as pypath:
        pypath.list_all_paths()
        expected_paths = set(p for p in sys.path if len(p))
        result = set(p for p in pypath.output_buffer.split() if len(p))
        assert_equal(result, expected_paths)


def test_print_pypath_file_path():
    with pypath_test_environment() as pypath:
        pypath.print_path_file()
        assert pypath.output[-1].endswith(MOCK_PATH_FILE)


def test_add_current_directory():
    with pypath_test_environment() as pypath:
        pypath.add_path()
        pypath.assert_paths_match([get_current_directory()])


def test_add_and_remove():
    with pypath_test_environment() as pypath:
        pypath.add_path()
        pypath.delete_path()
        assert_equal(len(pypath.current_custom_paths), 0)


# -------------------------------------------------------------------------
#  Test `add_path`
# -------------------------------------------------------------------------

def test_add_multiple_directories():
    with pypath_test_environment() as pypath:
        pypath.add_path()
        with cd_temp_directory('_dummy_'):
            pypath.add_path()
        assert_equal(len(pypath.current_custom_paths), 2)
        pypath.assert_paths_match(['.', '_dummy_'])


def test_add_absolute_path_input():
    with pypath_test_environment() as pypath:
        current_directory = get_current_directory()
        pypath.add_path(current_directory)
        pypath.assert_paths_match([current_directory])


def test_add_relative_path_input():
    with make_temp_dirs(['./_dummy_']):
        with pypath_test_environment() as pypath:
            pypath.add_path('_dummy_')
            pypath.assert_paths_match(['_dummy_'])


@raises(RuntimeError)
def test_add_nonexistent_path():
    with pypath_test_environment() as pypath:
        pypath.add_path('path/that/does/not/exist')


# -------------------------------------------------------------------------
#  Test `delete_path`
# -------------------------------------------------------------------------

def test_delete_index():
    user_paths = ['a/b/c', 'd/e/f', 'g/h', 'i/j']
    with pypath_test_environment(user_paths=user_paths) as pypath:
        pypath.delete_path('1')
        user_paths.pop(1)
        pypath.assert_paths_match(user_paths)


def test_delete_relative_path():
    user_paths = ['a/b/c', 'd/e/f', 'g/h', 'i/j']
    with pypath_test_environment(user_paths=user_paths) as pypath:
        pypath.delete_path('d/e/f')
        user_paths.pop(1)
        pypath.assert_paths_match(user_paths)


@raises(RuntimeError)
def test_delete_nonexistent_path():
    with pypath_test_environment() as pypath:
        pypath.delete_path('path/that/does/not/exist')


@raises(RuntimeError)
def test_delete_nonexistent_index():
    with pypath_test_environment() as pypath:
        pypath.delete_path('1')
