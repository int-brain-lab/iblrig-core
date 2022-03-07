import json
import logging
import os

from sys import platform, exit

# configure logging based on platform TODO: move elsewhere
INSTALL_LOG_PATH = ''
if platform == "linux" or platform == "linux2":
    INSTALL_LOG_PATH = '/tmp/iblrig-core.log'
elif platform == "win32":
    if not os.path.isdir('C:\\Temp'):
        os.mkdir('C:\\Temp')
    INSTALL_LOG_PATH = 'C:\\Temp\\iblrig-core.log'
else:
    logging.warning('Operating system not supported, exiting...')
    exit()

with open(INSTALL_LOG_PATH, 'w'):
    pass
logging.basicConfig(filename=INSTALL_LOG_PATH, level=logging.DEBUG)


def parameter_file_locator(path_to_file="C:\\iblrig_params\\.iblrig_params.json"):
    """
    Used to find and verify parameter file exists. Parameter file initially created by iblrig
    install script (TODO: double check what actually creates the file)

    Parameters
    ------
    path_to_file: str of file location, defaults to "C:\\iblrig_params\\.iblrig_params.json"

    Returns
    ------
    str of the path to the .iblrig_params.json file

    """
    file_exists = os.path.exists(path_to_file)
    if file_exists:
        return path_to_file
    else:
        logging.debug('Could not find the .iblrig_params.json file.')
        exit()  # or assume suitable defaults?


def determine_session_number(subject_folder_local="C:\\iblrig_data\\Subjects",
                             subject_folder_remote="Y:\\Subjects",
                             subject_name="test_mouse"):
    """
    Used to determine the correct session number.
    "C:\\iblrig_data\\Subjects\\test_mouse\\1900-01-01\\001"
    TODO: flesh out function elsewhere, similar logic to path_helper in iblrig
    
    Parameters
    ------
    subject_folder_local: str of local data folder, defaults to "C:\\iblrig_data\\Subjects"
    subject_folder_remote: str of remote data folder, defaults to "Y:\\Subjects"
    subject_name: str of subject name, default to "test_mouse"

    Returns
    ------
    session number for the subject in a str format, i.e. '001', '002'

    """
    local_folder_exists = os.path.isdir(subject_folder_local)
    remote_folder_exists = os.path.isdir(subject_folder_remote)

    if local_folder_exists and not remote_folder_exists:
        # Create local subject/date/number folder,
        subject_dir = os.path.join(subject_folder_local, subject_name)
        if os.path.isdir(subject_dir):
            # TODO: determine number as we are doing currently
            pass
        else:
            # first recording for this subject
            return '001'

    return '001'  # value hardcoded just for testing


def metadata_file_location(subject_name:str, date_directory:str, session_number:str, modality:str):
    """
    Used to determine where to store the metadata file.
    "C:\\iblrig_data\\Subjects\\test_mouse\\1900-01-01\\001\\raw_ephys_data\\session_metadata.yaml"

    Parameters
    ------
    subject_name: str of name of the subject, i.e. 'test_mouse'
    date_directory: str of date direcotry, i.e. '1900-01-01'
    session_number: str of current session number, i.e. '001'
    modality: str of modality in use, i.e. 'ephys'

    Returns
    ------
    str of the path where session_metadata.yaml will be created
    """
    return "C:\\iblrig_data\\Subjects\\test_mouse\\1900-01-01\\001\\raw_ephys_data\\session_metadata.yaml"


def metadata_set_subject():
    """Sets the subject parameter within the metadata file"""
    pass


def metadata_set_date():
    """Sets the date parameter within the metadata file"""
    pass


def metadata_set_session_number():
    """Sets the session_number parameter within the metadata file"""
    pass


def metadata_file_exists():
    """A check for whether the metadata file already exists with valid data"""
    pass


def metadata_write_to_file():
    """Attempt to write data to the metadata file"""
    pass


def metadata_set_rel_path():
    pass  # Rel_path : subject_name / date / number


def metadata_set_modality():
    pass  # Modality : [video | ephys | behavior | ...]


def metadata_set_acquisition_start():
    pass  # Acquisition_start: 2022 - 02 - 07T13: 46:35.236268


def metadata_set_acquisition_stop():
    pass  # Acquisition_stop: 2022 - 02 - 07T13: 46:35.236269


def metadata_set_files_for_extraction():
    pass  # Files_for_extraction: [‘file1.csv’, ‘file2.avi’, ...]


def metadata_set_server_status():
    pass  # Server_status: [present | absent]


def metadata_set_repo_hash():
    # here = os.getcwd()
    # os.chdir(folder)
    # out = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    # os.chdir(here)
    # if not out:
    #     log.debug("Commit hash is empty string")
    # log.debug(f"Found commit hash {out}")
    # return out
    pass  # Repo_hash / version: some_hash


def metadata_set_local_data_folder():
    pass  # Local_data_folder: C:\iblrig_data\Subjects


def metadata_set_remote_data_folder():
    pass  # Remote_data_folder: Y:\Subjects


def metadata_set_python_version():
    pass  # Python_version: 3.7 | 3.8 | 3.9...


def metadata_set_pip_freeze_output():
    pass  # Pip_freeze_output: [‘click >= 7.0.0’, ‘colorlog >= 4.0.2’, ‘flake8 >= 3.7.8’, ...]


if __name__ == '__main__':
    # Find the parameter file, verify it exists
    parameter_file_location = parameter_file_locator("/tmp/.iblrig_params.json")

    # Read the content of the parameter file
    json_data = json.loads(open(parameter_file_location).read())

    # Get subject name, separate function call? user prompt?
    mouse_name = "test_mouse"

    # Determine session number
    # determine_session_number((json_data['DATA_FOLDER_LOCAL']+"\\Subjects"),
    #                          (json_data['DATA_FOLDER_REMOTE']+"\\Subjects"),
    #                          mouse_name)
    determine_session_number('/tmp/', '/remotedatafolder/', mouse_name)

    # Create directories if required
    # os.makedirs(full_directory_path, exist_ok=True)

    # Determine location for the metadata file to be stored
    # "C:\\iblrig_data\\Subjects\\test_mouse\\1900-01-01\\001\\raw_ephys_data\\session_metadata.yaml"
    metadata_file_location('test_mouse', '1900-01-01', '001', 'ephys')

    # Set parameters to be stored into the metadata file:
    metadata_set_subject()  # Subject : <subject_name>
    metadata_set_date()  # Date : <date>
    metadata_set_session_number()  # Session_number : <session_number>
    metadata_set_rel_path()  # Rel_path : subject_name / date / number
    metadata_set_modality()  # Modality : [video | ephys | behavior | ...]
    metadata_set_acquisition_start()  # Acquisition_start: 2022 - 02 - 07T13: 46:35.236268
    metadata_set_acquisition_stop()  # Acquisition_stop: 2022 - 02 - 07T13: 46:35.236269
    metadata_set_files_for_extraction()  # Files_for_extraction: [‘file1.csv’, ‘file2.avi’, ...]
    metadata_set_server_status()  # Server_status: [present | absent]
    metadata_set_repo_hash()  # Repo_hash / version: some_hash
    metadata_set_local_data_folder()  # Local_data_folder: C:\iblrig_data\Subjects
    metadata_set_remote_data_folder()  # Remote_data_folder: Y:\Subjects
    metadata_set_python_version()  # Python_version: 3.7 | 3.8 | 3.9...
    metadata_set_pip_freeze_output()  # Pip_freeze_output: [‘click >= 7.0.0’, ‘colorlog >= 4.0.2’]
    # TODO:
    #  Create getter functions
    #  Get list of hardware and Windows patch level?

    # check if metadata file already exists and contains valid data
    metadata_file_exists()
    # write data to the metadata file
    metadata_write_to_file()
