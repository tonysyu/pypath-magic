import os
import sys
from contextlib import contextmanager

from pypath_magic import PathMagic, join_with_site_packages_dir


#--------------------------------------------------------------------------
#  Test helpers
#--------------------------------------------------------------------------


MOCK_PATH_FILE = '_pypath_test_path_.pth'


class TestablePathMagic(PathMagic):

    def __init__(self, *args, **kwargs):
        super(TestablePathMagic, self).__init__(*args, **kwargs)
        self._output = []
        self.path_file = join_with_site_packages_dir(MOCK_PATH_FILE)

    def __call__(self, *args, **kwargs):
        self.pypath(*args, **kwargs)

    def write(self, line):
        """Override write method to save lines instead of printing."""
        self._output.append(line)

    @property
    def output_buffer(self):
        return '\n'.join(self._output)

    @property
    def output_lines(self):
        return self.output_buffer.split('\n')

    @property
    def last_output(self):
        return self.output_lines[-1]

    @property
    def current_custom_paths(self):
        self('')  # Calling `pypath` with no arguments lists custom paths.
        lines = self._output.pop()
        if len(lines.strip()):
            return lines.split('\n')
        else:
            return []


@contextmanager
def cd(path):
    """Temporarily change directory."""
    original_path = os.getcwdu()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_path)


@contextmanager
def temp_dir(path):
    """Temporarily add directory."""
    os.mkdir(path)
    try:
        yield
    finally:
        os.removedirs(path)


@contextmanager
def cd_temp_directory(path):
    with temp_dir(path):
        with cd(path):
            yield


@contextmanager
def pypath_test_environment():
    pypath = TestablePathMagic()
    try:
        yield pypath
    finally:
        if os.path.isfile(pypath.path_file):
            os.remove(pypath.path_file)


#--------------------------------------------------------------------------
#  Tests
#--------------------------------------------------------------------------

def test_empty():
    with pypath_test_environment() as pypath:
        pypath('')
        assert pypath.output_buffer == ''


def test_list_all_paths():
    with pypath_test_environment() as pypath:
        pypath('-l')
        expected_paths = set(p for p in sys.path if len(p))
        result = set(p for p in pypath.output_buffer.split() if len(p))
        assert result == expected_paths


def test_print_pypath_file_path():
    with pypath_test_environment() as pypath:
        pypath('-p')
        assert pypath.last_output.endswith(MOCK_PATH_FILE)


def test_add_current_directory():
    with pypath_test_environment() as pypath:
        pypath('-a')
        assert pypath.current_custom_paths[0] == os.getcwdu()


def test_add_multiple_directories():
    with pypath_test_environment() as pypath:
        pypath('-a')
        with cd_temp_directory('_dummy_'):
            pypath('-a')
        assert len(pypath.current_custom_paths) == 2
        assert pypath.current_custom_paths[-1].endswith('_dummy_')


def test_add_and_remove():
    with pypath_test_environment() as pypath:
        pypath('-a')
        pypath('-d')
        assert len(pypath.current_custom_paths) == 0
