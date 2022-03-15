import json
import logging
import os

from datetime import datetime
from pathlib import Path
from subprocess import check_output, CalledProcessError
from sys import exit, version
from traceback import print_stack

log = logging.getLogger("iblrig")
PARAMS_FILE_PATH = Path().home().joinpath(".iblrigcore_params.json")


def parameter_file_locator(file_path=PARAMS_FILE_PATH):
    """
    Used to find and verify parameter file exists. Parameter file initially created by iblrig
    install script (TODO: refactor to use the ParamFile class read method)

    Parameters
    ------
    file_path: str of file location, defaults to variable PARAMS_FILE_PATH

    Returns
    ------
    str of the path to the .iblrigcore_params.json file

    """
    file_exists = os.path.exists(file_path)
    if file_exists:
        return file_path
    else:
        logging.debug('Could not find the .iblrigcore_params.json file.')
        print_stack()
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

    return '001'  # value hardcoded for testing


def metadata_file_location(subject_name: str, date_directory: str, session_number: str,
                           modality: str, server_present=False):
    """
    Used to determine where to store the metadata file.
    "C:\\iblrig_data\\Subjects\\test_mouse\\1900-01-01\\001\\raw_ephys_data\\session_metadata.json"

    Parameters
    ------
    subject_name: str of name of the subject, i.e. 'test_mouse'
    date_directory: str of date directory, i.e. '1900-01-01'
    session_number: str of current session number, i.e. '001'
    modality: str of modality in use, i.e. 'ephys'
    server_present: bool to determine output session directly to server (Y:\\ drive)

    Returns
    ------
    str of the path where session_metadata.json will be created
    """
    if server_present:
        subjects_dir = "Y:\\Subjects"
    else:
        subjects_dir = "C:\\iblrig_data\\Subjects"
    modality = "raw_"+modality+"_data"
    metadata_file_loc = os.path.join(subjects_dir, subject_name, date_directory, session_number,
                                     modality, "session_metadata.json")
    return metadata_file_loc


def metadata_get_json_values(file_path: str):
    """
    Reads in the contents of the given json file, perform any requisite validations, and returns a
    dict of the relevant data.

    Parameters
    ------
    file_path: str of the location of the metadata json file

    Returns
    ------
    dict of all values found in the metadata json file
    """
    if os.path.exists(file_path):
        metadata_dict = json.loads(file_path)
        # perform any requisite validations here, expected values present?
        return metadata_dict
    else:
        # file does not currently exist, return empty dict
        return {}


def get_subject_name():
    """
    Gets the subject name value

    Returns
    ------
    str: subject name 'test_mouse'
    """
    # TODO: Ask user for name, query file that contains the data, or call function
    subject_name = 'test_mouse'
    return subject_name


def get_date():
    """
    Gets the datetime value in the preferred format

    Returns
    ------
    str: datetime for now as a string, i.e. '1900-01-01 14:04:02'
    """
    our_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return our_datetime


def get_session_number():
    """
    Gets the session_number value

    Returns
    ------
    str: session number, i.e. '001'
    """
    # TODO: query file that contains the data or call function
    session_number = '001'
    return session_number


def get_rel_path():
    """
    Get the relative path value for the subject

    Returns
    ------
    str: relative path, i.e. 'test_mouse/1901-01-01/001'
    """
    # TODO: query file that contains the data or call function
    rel_path = 'test_mouse/1901-01-01/001'
    return rel_path


def get_modality():
    """
    Get the modality value for what is currently in use

    Returns
    ------
    str: modality, i.e. 'ephys'
    """
    # TODO: query file that contains the data or call function
    modality = 'ephys'
    return modality


def get_acquisition_start():
    """
    Get the acquisition start datetime value in datetime.isoformat

    Returns
    ------
    str: datetime of acquisition start, i.e. '2022-02-07T13:46:35.236268'
    """
    # TODO: query file that contains the data or call function
    acquisition_start = datetime.now().isoformat()
    return acquisition_start


def get_acquisition_stop():
    """
    Get the acquisition stop datetime value in datetime.isoformat

    Returns
    ------
    str: datetime of acquisition stop, i.e. '2022-02-07T13:46:35.236268'
    """
    # TODO: query file that contains the data or call function
    acquisition_stop = datetime.now().isoformat()
    return acquisition_stop


def get_files_for_extraction():
    """
    Get the list of filenames for extraction

    Returns
    ------
    list: list of filenames that will require extraction, i.e. [‘file1.csv’, ‘file2.avi’, ...]
    """
    # TODO: query file that contains the data or call function
    filename_list = ['file1.csv', 'file2.avi']
    return filename_list


def get_server_status():
    """
    Get the server status

    Returns
    ------
    str: server status, i.e. 'present' or 'absent'
    """
    # TODO: query file that contains the data or call function
    server_status = 'absent'
    return server_status


def get_repo_hash():
    """
    Get the repository hash

    Returns
    ------
    str: repository hash, i.e. 'db39a35aa13c93f553a686cb5a5f662c9406663e'
    """
    try:
        repo_hash = check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        return repo_hash
    except CalledProcessError:
        log.debug(CalledProcessError, print_stack())


def get_local_data_folder():
    """
    Get the local data folder path

    Returns
    ------
    str: local data folder path, i.e. 'C:\\iblrig_data'
    """
    # TODO: query file that contains the data or call function
    local_data_folder = 'C:\\iblrig_data'
    return local_data_folder


def get_remote_data_folder():
    """
    Get the remote data folder path

    Returns
    ------
    str: remote data folder path, i.e. 'Y:\\'
    """
    # TODO: query file that contains the data or call function
    remote_data_folder = 'Y:\\'
    return remote_data_folder


def get_python_version():
    """
    Get the currently running version of python

    Returns
    ------
    str: python version, i.e. '3.7.12'
    """
    python_version = version.split()[0]
    return python_version


def get_pip_freeze_output():
    """
    Get the output from a pip freeze command

    Returns
    ------
    list: containing strings, i.e. ['attrs==21.4.0', 'iniconfig==1.1.1', 'packaging==21.3'...]
    """
    try:
        pip_freeze = check_output(["pip", "freeze"]).decode().split()
        if not pip_freeze:
            log.debug("Running the 'pip freeze' command did not have expected results.\n",
                      print_stack())
        return pip_freeze
    except CalledProcessError:
        log.debug(CalledProcessError, print_stack())


def metadata_write_to_file(dict_data: dict, file_path: str):
    """
    Attempt to write dictionary data to the metadata file at the given file location

    Parameters
    ------
    dict_data: dictionary data that will be written to the metadata json file
    file_path: location of the file to be written to

    Returns
    ------
    bool: True for success, False for failure
    """

    if os.path.exists(file_path):
        # TODO: throw error b/c the file already exists? simply overwrite? perform validation?
        # print_stack()
        return False
    else:
        try:
            with open(file_path, 'w') as fp:
                json.dump(dict_data, fp)
        except IOError:
            log.debug(IOError, print_stack())
        return True


def main():
    # Find the parameter file, verify it exists
    parameter_file_location = parameter_file_locator("/tmp/.iblrig_params.json")

    # Read the content of the parameter file
    parameter_dict_data = json.loads(open(parameter_file_location).read())

    # Get subject name, separate function call? user prompt?
    mouse_name = "test_mouse"

    # Determine session number
    # determine_session_number((parameter_dict_data['DATA_FOLDER_LOCAL']+"\\Subjects"),
    #                          (parameter_dict_data['DATA_FOLDER_REMOTE']+"\\Subjects"),
    #                          mouse_name)
    dsn = determine_session_number('/tmp/', '/remotedatafolder/', mouse_name)

    # ddd = determine_date_directory()
    # dm = determine_modality()
    # dsp = determine_server_present()

    # Create (sub)directories if required
    # os.makedirs(full_directory_path, exist_ok=True)

    # Determine location for the metadata file to be stored
    # "C:\\iblrig_data\\Subjects\\test_mouse\\1900-01-01\\001\\raw_ephys_data\\session_metadata.json"
    # mdfl = metadata_file_location(mouse_name, ddd, dsn, dm, dsp)
    mdfl = metadata_file_location(mouse_name, '1900-01-01', '001', 'ephys', False)

    # Read in json values
    md_dict = metadata_get_json_values(mdfl)

    # Set values to be stored into the metadata file:
    md_dict['Subject_name'] = get_subject_name()
    md_dict['Date'] = get_date()
    md_dict['Session_number'] = get_session_number()
    md_dict['Rel_path'] = get_rel_path()
    md_dict['Modality'] = get_modality()
    md_dict['Acquisition_start'] = get_acquisition_start()
    md_dict['Acquisition_stop'] = get_acquisition_stop()
    md_dict['Files_for_extraction'] = get_files_for_extraction()
    md_dict['Server_status'] = get_server_status()
    md_dict['Repo_hash'] = get_repo_hash()
    md_dict['Local_data_folder'] = get_local_data_folder()
    md_dict['Remote_data_folder'] = get_remote_data_folder()
    md_dict['Python_version'] = get_python_version()
    md_dict['Pip_freeze_output'] = get_pip_freeze_output()
    # TODO: Get list of hardware and Windows patch level?

    # write data to the metadata file
    metadata_write_to_file(md_dict, mdfl)


if __name__ == "__main__":
    main()
