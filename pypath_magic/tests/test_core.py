import os

from pypath_magic.testing import (BasicPyPathInterface, PyPathAddInterface,
                                  PyPathDeleteInterface, TestablePyPath,
                                  MOCK_PATH_FILE)


class TestHarness(object):

    def setup(self):
        self.pypath = TestablePyPath(pypath_filename=MOCK_PATH_FILE)

    def teardown(self):
        if os.path.isfile(self.pypath.path_file):
            os.remove(self.pypath.path_file)


class TestBasicPyPathInterface(TestHarness, BasicPyPathInterface):
    pass


class TestPyPathAddInterface(TestHarness, PyPathAddInterface):
    pass


class TestPyPathDeleteInterface(TestHarness, PyPathDeleteInterface):
    pass
