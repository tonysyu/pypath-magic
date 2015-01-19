import os
import sys

from nose.tools import assert_in, assert_not_in
from IPython.core.error import UsageError

from pypath_magic.utils import get_current_directory
from pypath_magic.ipymagic import IPyPath, PathMagic
from pypath_magic.testing import (MOCK_PATH_FILE, BasicPyPathInterface,
                                  PyPathAddInterface, PyPathDeleteInterface,
                                  TestablePyPath, cd_temp_directory)


class TestableIPyPath(TestablePyPath, IPyPath):

    pass


class PathMagicAsPyPath(PathMagic):
    """Adapt `PathMagic` class to standard PyPath interface.
    """

    def __init__(self, *args, **kwargs):
        super(PathMagicAsPyPath, self).__init__(*args, **kwargs)
        self._pypath_cmd = TestableIPyPath()

    @property
    def path_file(self):
        return self._pypath_cmd.path_file

    @property
    def current_custom_paths(self):
        return self._pypath_cmd._load_user_paths()

    @property
    def output(self):
        return self._pypath_cmd.output

    @property
    def output_buffer(self):
        return self._pypath_cmd.output_buffer

    def add_path(self, path=''):
        self.pypath('-a {}'.format(path))

    def delete_path(self, path=''):
        self.pypath('-d {}'.format(path))

    def list_custom_paths(self):
        self.pypath('')

    def list_all_paths(self):
        self.pypath('-l')

    def print_path_file(self):
        self.pypath('-p')


class TestHarness(object):

    def setup(self):
        self.pypath = PathMagicAsPyPath(pypath_filename=MOCK_PATH_FILE)

    def teardown(self):
        if os.path.isfile(self.pypath.path_file):
            os.remove(self.pypath.path_file)


class TestBasicPyPathInterface(TestHarness, BasicPyPathInterface):

    def test_add_current_directory_changes_sys_path(self):
        # The PyPath magic command should alter the active sys.path.
        with cd_temp_directory('_dummy_'):
            self.pypath.add_path()
            assert_in(get_current_directory(), sys.path)

    def test_add_and_remove_changes_sys_path(self):
        # The PyPath magic command should alter the active sys.path.
        with cd_temp_directory('_dummy_'):
            self.pypath.add_path()
            self.pypath.delete_path()
            assert_not_in(get_current_directory(), sys.path)


class TestPyPathAddInterface(TestHarness, PyPathAddInterface):

    error_class = UsageError


class TestPyPathDeleteInterface(TestHarness, PyPathDeleteInterface):

    error_class = UsageError
