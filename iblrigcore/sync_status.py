#!/usr/bin/env python
# @File: iblrigcore/sync_status.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, February 23rd 2022, 4:21:36 pm
from pathlib import Path
import csv
from datetime import datetime
import inspect


def timestamp() -> str:
    """_summary_: Returns a timestamp.

    Returns:
        str: timestamp ISO formatted string
    """
    return datetime.now().isoformat()


def computer_name() -> str:
    return "myPC"


def caller(fullpath: bool = True) -> str:
    """returns the filename/caller of the function calling this function

    Args:
        fullpath (bool, optional): return the full path of the module.
                               Defaults to True.

    Returns:
        str: fullpath/caller_name OR filename/caller_name
    """
    stack = inspect.stack()
    name = stack[1][3]  # caller's name or stack[1].function
    fname = stack[1][0].f_code.co_filename
    # name = stack[1][0].f_code.co_name
    # locals_ = stack[1][0].f_locals
    del stack
    short_name = "/".join([Path(fname).name, name])
    long_name = "/".join([fname, name])
    return short_name if not fullpath else long_name


def create_status_file(session_path: Path) -> None:
    """_summary_: Creates an empty status file in the session folder just with a header.

    Args:
        session_path (Path): A path object of the remote session that starting to acquire data.
    """
    session_path = Path(session_path)
    status_file = session_path.joinpath("session_status.csv")
    if status_file.exists():
        print("status file already exists")
        return
    header = ["Timestamp", "ComputerName", "Caller", "Status"]
    row = [timestamp(), computer_name(), caller(), "created_status_file"]
    with open(status_file, "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write multiple rows
        writer.writerow(row)

    return status_file.absolute()


def load_status_file(session_path: Path) -> dict:
    """_summary_: Loads the status file of the session

    Args:
        session_path (Path): A path object of the remote session.

    Returns:
        dict: Loaded status_file.json
    """
    session_path = Path(session_path)
    status_file = session_path.joinpath("session_status.json")
    if not status_file.exists():
        print("status file does not exist")
        return {}
    with open(status_file, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    create_status_file(".")

