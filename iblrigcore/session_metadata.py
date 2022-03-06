import logging
import os

# configure logging
if not os.path.isdir('C:\\Temp'):
    os.mkdir('C:\\Temp')
INSTALL_LOG_PATH = 'C:\\Temp\\iblrig-core.log'
with open(INSTALL_LOG_PATH, 'w'):
    pass
logging.basicConfig(filename=INSTALL_LOG_PATH, level=logging.DEBUG)


def parameter_file_locator(path_to_file = "C:\\iblrig_params\\.iblrig_params.json"):
    """
    Used to find parameter file (C:\iblrig_params\.iblrig_params.json)
    Parameter file initially created by iblrig install script

    Returns
    ------

    """
    file_exists = os.path.exists(path_to_file)
    if file_exists:
        return path_to_file
    else:
        # log and throw error, or find suitable defaults?
        pass



def parameter_file_reader():
    """Reads in the content of the parameter file"""
    pass


def metadata_file_location():
    """Sets the location to store the metadata file"""
    pass


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


if __name__ == '__main__':
    # find the parameter file
    parameter_file_locator()
    # read the content of the parameter file
    parameter_file_reader()
    # Determine location for the metadata file to be stored.
    metadata_file_location()
    # Set parameters to be stored into the metadata file:
    metadata_set_subject()  # Subject : <subject_name>
    metadata_set_date()  # Date : <date>
    metadata_set_session_number()  # Session_number : <session_number>
    # ... etc ...
    # check if metadata file already exists and contains valid data
    metadata_file_exists()
    # write data to the metadata file
    metadata_write_to_file()
    # TODO:
    #  Create getter functions
    pass
    