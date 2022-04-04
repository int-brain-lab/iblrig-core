#!/usr/bin/env python
# @File: iblrigcore/session_number.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Thursday, March 31st 2022, 6:34:46 pm
"""
This module should implements all necessary logic to determine the a session's relative path.
A session's relative path has the format: mousename/date/number where:
- mousename is a user input,
- date is the current date,
- number is automatically deduced from the system by looking into the DATA_FOLDER_LOCAL and
DATA_FOLDER_REMOTE entries of the existing ParamFile.

DATA_FOLDER_LOCAL and DATA_FOLDER_REMOTE are used as root paths for the same relative path.

To determine the session number of a session:
Look into the DATA_FOLDER_REMOTE for a folder with the inputted mousename/date:
- If it does not exist: create a mousename/date/001 folder into the DATA_FOLDER_REMOTE
    - Create a sync_sttus.csv file into the newly created folder
    - log the file creation and the creation of the folder into the sync_status.csv file
- If mousename/date exists: list the mousename/date subfolders and find the highest number
    - Determine if this session is a running session or if it has already completed using the
    sync_status.csv file.
    - If it's a currently running session, ask the user if they want to attach tho this session
    - If it's not a currently running session, create a folder under
    DATA_FOLDER_REMOTE/mousename/date with the number highest number (found previously) + 1
    If no number was found use 001
Create corresponding DATA_FOLDER_LOCAL/mousename/data/number folder
Crearte in DATA_FOLDER_LOCAL/mousename/data/number a raw_<modality>_data folder where modality
comes from the ParamFile.


Session data is collected on a local rig and then transferred to the local server
using the REMOTE_DATA_FOLDER root path and the current session relative path.


"""
from iblrigcore.params import ParamFile
from pathlib import Path


def get_session_number(mousename):
    """
    This function should return the session number of the current running session.
    Or the new session number if no session is running.
    """
    pars = ParamFile.read()


def list_mouse_sessions(mousename, folder_type="remote"):
    """
    This function should return a list of all the sessions of the inputted mousename.
    """
    pars = ParamFile.read()
    if folder_type == "remote":
        root_folder = pars["DATA_FOLDER_REMOTE"]
    elif folder_type == "local":
        root_folder = pars["DATA_FOLDER_LOCAL"]
    elif isinstance(folder_type, Path):
        root_folder = folder_type
    else:
        raise ValueError("folder_type must be either 'remote', 'local', or a Path object")
    root_folder = Path(root_folder)
    mouse_folder = root_folder.joinpath(mousename)
    if not mouse_folder.exists():
        return []
    sessions =  [p for p in mouse_folder.rglob("*") if len(p.name) == 3 and p.name.isdecimal()]

    return sessions