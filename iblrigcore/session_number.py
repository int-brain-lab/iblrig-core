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
look into the DATA_FOLDER_REMOTE for a folder with the inputted mousename/date:
- If it does not exist: create a mousename/date/001 folder into the DATA_FOLDER_REMOTE
- If mousename/date exists: list the mousename/date subfolders and find the highest number
- Determine if this session is a running session or if it has already completed using the
sync_status.csv file.
- If the session is not currently running, create a fodler under mousename/date with the number


Session data is collected on a local rig and then transferred to the local server
using the REMOTE_DATA_FOLDER root path and the current session relative path.


"""
