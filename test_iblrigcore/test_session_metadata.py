import json
import os
import tempfile
import unittest
from datetime import datetime

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

    def test_determine_session_number(self):
        assert False

    def test_metadata_file_location(self):
        assert False

    def test_metadata_get_json_values(self):
        assert False

    def test_get_subject_name(self):
        assert False

    def test_get_date(self):
        test_date = sm.get_date()
        self.assertTrue(isinstance(test_date, str))
        test_datetime_object = datetime.strptime(test_date, '%Y-%m-%d %H:%M:%S')
        self.assertTrue(isinstance(test_datetime_object, datetime))

    def test_get_session_number(self):
        assert False

    def test_get_rel_path(self):
        assert False

    def test_get_modality(self):
        # TODO: call some function to get list of modalities
        #  - modality_list = get_modality_list()
        modality_list = ['ephys', 'video', 'behavior', 'training', 'etc']
        modality = sm.get_modality()
        self.assertTrue(isinstance(modality, str))
        if modality not in modality_list:
            assert False

    def test_get_acquisition_start(self):
        assert False

    def test_get_acquisition_stop(self):
        assert False

    def test_get_files_for_extraction(self):
        assert False

    def test_get_server_status(self):
        assert False

    def test_get_repo_hash(self):
        self.assertTrue(isinstance(sm.get_repo_hash(), str))

    def test_get_local_data_folder(self):
        local_data_folder = sm.get_local_data_folder()
        self.assertTrue(isinstance(local_data_folder, str))
        if not os.path.exists(os.path.dirname(local_data_folder)):
            assert False

    def test_get_remote_data_folder(self):
        remote_data_folder = sm.get_remote_data_folder()
        self.assertTrue(isinstance(remote_data_folder, str))
        if not os.path.exists(os.path.dirname(remote_data_folder)):
            assert False

    def test_get_python_version(self):
        self.assertTrue(isinstance(sm.get_python_version(), str))

    def test_get_pip_freeze_output(self):
        pip_freeze_output = sm.get_pip_freeze_output()
        self.assertTrue(isinstance(pip_freeze_output, list))
        if pip_freeze_output:
            for item in pip_freeze_output:
                self.assertTrue(isinstance(item, str))

    def test_metadata_write_to_file(self):
        test_dict = {1: 'test', 2: 'dict', 3: 'values'}
        test_tempfile = tempfile.NamedTemporaryFile()
        test_fake_file = '/tmp/test_fake_file.json'
        self.assertFalse(sm.metadata_write_to_file(test_dict, test_tempfile.name))
        self.assertTrue(sm.metadata_write_to_file(test_dict, test_fake_file))
        test_json_file_content = json.loads(open(test_fake_file).read())
        self.assertTrue(isinstance(test_json_file_content, dict))
