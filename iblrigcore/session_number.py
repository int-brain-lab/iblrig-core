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
from datetime import datetime
from dateutil import parser
from typing import Tuple, Union


def session_path_sort_func(p: Path) -> Tuple[datetime, int]:
    """Sort session paths by subject, parsed date, and number

    Args:
        p (Path): valid session_path ending in subject/date/number

    Returns:
        Tuple[datetime, int]: date and number of a session path object
    """
    p = Path(p)
    subj = p.parts[-3]
    date = p.parts[-2]
    # Some date folders might have a '_' in them, so we need to remove it
    if "_" in date:
        date = date.replace("_", ":")
    date = parser.parse(date)
    number = int(p.parts[-1])
    return subj, date, number


def is_session_path(p: Path) -> bool:
    """Check if a path or a string is a valid session path.
    Will skip the check for dir if Path does not exist.
    A session path is defined as any folder under the root_folder with the format:
    mousename/date/number.
    No way currently to check if mousename is a valid mouse name without more info
    or checking the DB.

    Args:
        p (Path): path to check, can be a folder or a file

    Returns:
        bool: True if the path is a valid session path, False otherwise
    """
    p = Path(p)
    # Must be a directory
    if p.exists() and not p.is_dir():
        return False
    # Must be a length 3 name composed by base 10 digits
    if not p.parts[-1].isdecimal():
        return False
    if len(p.parts[-1]) != 3:
        return False
    # Must be a valid isoformatted date string
    try:
        parser.parse(p.parts[-2])
    except ValueError:
        return False
    return True


def list_sessions(root_folder: Union[str, Path]) -> list:
    """This function should return a list of all the sessions paths of all the mice.

    Args:
        root_folder (Union[str, Path]): Root Subjects/ data folder, usually
                                        DATA_FOLDER_LOCAL or DATA_FOLDER_REMOTE

    Returns:
        list: list of session paths sorted by date and number
    """
    # Parsed 177466 paths in 3.2528727054595947 seconds
    # Parsed 2421933 paths in 51.873934745788574 seconds
    # Parsed 2422126 paths in 46.614375829696655 seconds
    root_folder = Path(root_folder)
    sessions = [p for p in root_folder.rglob("*") if is_session_path(p)]
    sessions.sort(key=session_path_sort_func)
    return sessions


def list_mouse_sessions(root_folder: Union[str, Path], mousename: str) -> list:
    """This function should return a list of all the sessions paths of the inputted mousename.

    Args:
        mousename (str): mouse name
        root_folder (Union[str, Path]): Root Subjects/ data folder, usually
                                        DATA_FOLDER_LOCAL or DATA_FOLDER_REMOTE

    Returns:
        list: list of session paths sorted by date and number
    """
    root_folder = Path(root_folder)
    if root_folder.name.lower() == "subjects":
        subjects_path = root_folder
    else:
        subjects_path = root_folder.joinpath("Subjects")
        assert subjects_path.exists(), f"Cannot find a Subject's path in {root_folder}"
    mousename_path = subjects_path.joinpath(mousename)
    mouse_sessions = list_sessions(mousename_path)
    return mouse_sessions


def get_session_number(mousename):
    """
    This function should return the session number of the current running session.
    Or the new session number if no session is running.
    """
    pars = ParamFile.read()
    sessions_local = list_mouse_sessions(pars["DATA_FOLDER_LOCAL"], mousename)
    sessions_remote = list_mouse_sessions(pars["DATA_FOLDER_REMOTE"], mousename)
    all_mouse_sessions = list(set(sessions_local) | set(sessions_remote))
    all_mouse_sessions.sort(key=session_path_sort_func)
    latest_session = all_mouse_sessions[-1]
    if parser.parse(latest_session.parts[-2]).date() < datetime.now().date():
        return "001"
    elif parser.parse(latest_session.parts[-2]).date() == datetime.now().date():
        return str(int(latest_session.parts[-1]) + 1).zfill(3)
    else:
        raise ValueError(f"Latest session date is in the future: {latest_session}")


def new_session_paths(mousename: str, date: datetime, number: int) -> Tuple[Path, Path]:
    """Create the paths for a new session.

    Args:
        mousename (str): mouse name
        date (datetime): date of the session
        number (int): number of the session

    Returns:
        Tuple[Path, Path]: local and remote paths for the new session
    """
    pars = ParamFile.read()
    # Create the local session path
    local_session_path = (
        Path(pars["DATA_FOLDER_LOCAL"])
        .joinpath(mousename)
        .joinpath(date.strftime("%Y_%m_%d"))
        .joinpath(str(number).zfill(3))
    )
    # Create the remote session path
    remote_session_path = (
        Path(pars["DATA_FOLDER_REMOTE"])
        .joinpath(mousename)
        .joinpath(date.strftime("%Y_%m_%d"))
        .joinpath(str(number).zfill(3))
    )
    return local_session_path, remote_session_path
