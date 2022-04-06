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
import datetime
from dateutil import parser
from typing import Tuple, Union


def session_path_sort_func(p: Path) -> Tuple[datetime.datetime, int]:
    """Sort session paths by parsed date and number

    Args:
        p (Path): valid session_path ending in subject/date/number

    Returns:
        Tuple[datetime.datetime, int]: date and number of a session path object
    """
    p = Path(p)
    date = p.parts[-2]
    # Some date folders might have a '_' in them, so we need to remove it
    if "_" in date:
        date = date.replace("_", ":")
    date = parser.parse(date)
    number = int(p.parts[-1])
    return date, number


def is_session_path(p: Path) -> bool:
    """Check if a path is a valid session path.
    A session path is defined as any folder under the root_folder with the format:
    mousename/date/number.

    Args:
        p (Path): path to check

    Returns:
        bool: True if the path is a valid session path, False otherwise
    """
    # Must be a directory
    if not p.is_dir():
        return False
    # Must be a length 3 name composed by base 10 digits
    if not p.parts[-1].isdecimal():
        return False
    if len(p.parts[-1]) != 3:
        return False
    # Must be a valid date or datetime isoformatted
    # TODO: FINISH ME!
    return True


def list_mouse_sessions(mousename: str, root_folder: Union[str, Path]) -> list:
    """This function should return a list of all the sessions paths of the inputted mousename.

    Args:
        mousename (str): mouse name
        root_folder (Union[str, Path]): Root Subjects/ data folder, usually
                                        DATA_FOLDER_LOCAL or DATA_FOLDER_REMOTE

    Returns:
        list: list of session paths sorted by date and number
    """
    root_folder = Path(root_folder)
    mouse_folder = root_folder.joinpath(mousename)
    if not mouse_folder.exists():
        return []
    # Grab only folders that end in a 3 digit number
    sessions = [p for p in mouse_folder.rglob("*") if len(p.name) == 3 and p.name.isdecimal()]
    # sessions = sorted(sessions, key=lambda x: (parser.parse(x.parts[-2]), int(x.parts[-1])))
    # list.sort() is inplace and seems to be about 3% faster than sorted()
    sessions.sort(key=session_path_sort_func)
    return sessions


def get_session_number(mousename):
    """
    This function should return the session number of the current running session.
    Or the new session number if no session is running.
    """
    pars = ParamFile.read()


