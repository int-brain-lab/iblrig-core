#!/usr/bin/env python
# @File: iblrigcore/sync_status.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, February 23rd 2022, 4:21:36 pm
import csv
import inspect
import socket
from datetime import datetime
from pathlib import Path
from sys import flags

from iblrigcore.params import ParamFile


def modality() -> str:
    """return the name of the modality"""
    return ParamFile.read(key='MODALITY')


def timestamp() -> str:
    """_summary_: Returns a timestamp.

    Returns:
        str: timestamp ISO formatted string
    """
    return datetime.now().isoformat()


def computer_name() -> str:
    """_summary_: Returns the hostname of the computer

    Returns:
         str: host name of the computer
    """
    return socket.gethostname()


def caller(skip: int = 2) -> str:
    """Get a name of a caller in the format module.class.method

    Args:
        skip (int, optional): specifies how many levels of stack to skip while getting
            caller name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
            Defaults to 2.

    Returns:
        str: An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ""
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # module.name can be None when frame is executed directly in console
    # TODO: consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if "self" in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals["self"].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != "<module>":  # top level usually
        name.append(codename)  # function or a method

    ## Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return ".".join(name)


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
    header = ["Timestamp", "ComputerName", "Caller", "Modality", "Action"]
    # e.g. [2022-02-22T22:22:22:22.222222, IBLvideo, iblrig.iblrigcore.prepare_session, videoPC, start_acquisition]
    row = [timestamp(), computer_name(), caller(), modality(), "created_status_file"]
    with open(status_file, "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row)

    return status_file.absolute()


def load_status_file(session_path: Path, header: bool = True) -> dict:
    """_summary_: Loads the status file of the session

    Args:
        session_path (Path): A path object of the remote session.
        header (bool, optional): Retrun with header. Defaults to True.

    Returns:
        dict: Loaded status_file.json
    """
    session_path = Path(session_path)
    status_file = session_path.joinpath("session_status.csv")
    if not status_file.exists():
        print("status file does not exist")
        return {}
    with open(status_file, newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        head = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
    out = rows.copy()
    if header:
        out.insert(0, head)
    return out


def append_status_file(session_path: Path, action: str) -> None:
    """Append a line to the status file of the session

    Args:
        session_path (Path): _description_
        action (str): _description_
    """
    session_path = Path(session_path)
    status_file = session_path.joinpath("session_status.csv")
    if not status_file.exists():
        print("status file does not exist")
        return {}
    row = [timestamp(), computer_name(), caller(), modality(), action]
    with open(status_file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(row)
    return
