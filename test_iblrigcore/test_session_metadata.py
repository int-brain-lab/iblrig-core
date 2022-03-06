import tempfile
import unittest

import iblrigcore.session_metadata as sm


class TestSessionMetadata(unittest.TestCase):
    def test_parameter_file_locator(self):
        # test with a file that certainly exists
        test_tempfile = tempfile.NamedTemporaryFile()
        self.assertTrue(isinstance(sm.parameter_file_locator(test_tempfile.name), str))

        # test with a file that definitely does not exist
        # might need to be changed in the future
        definitely_not_a_file = 'this is definitely not an actual file'
        with self.assertRaises(SystemExit):
            sm.parameter_file_locator(definitely_not_a_file)

    def test_metadata_file_location(self):
        assert False

    def test_metadata_set_subject(self):
        assert False

    def test_metadata_set_date(self):
        assert False

    def test_metadata_set_session_number(self):
        assert False

    def test_metadata_file_exists(self):
        assert False

    def test_metadata_write_to_file(self):
        assert False
