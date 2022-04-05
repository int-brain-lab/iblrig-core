#!/usr/bin/env python
# @File: test_iblrigcore/test_session_number.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, April 4th 2022, 4:20:40 pm
from datetime import datetime
import tempfile
from pathlib import Path

from iblrigcore import sync_status
import iblrigcore.session_number as sn


#FIXME: import params and create then delete at end of test module
def create_fake_sessions(tempdir, mousename):
    tempdir_path = Path(tempdir.name)
    old = [mousename, "2000-01-01", "001"]
    old2 = [mousename, "2000-01-01", "002"]
    one = [mousename, datetime.now().date().isoformat(), "001"]
    two = [mousename, datetime.now().date().isoformat(), "002"]
    tempdir_path.joinpath(*old).mkdir(parents=True)
    tempdir_path.joinpath(*old2).mkdir(parents=True)
    tempdir_path.joinpath(*one).mkdir(parents=True)
    tempdir_path.joinpath(*two).mkdir(parents=True)
    # Create sync_status.csv files for each session
    for session in [old, old2, one, two]:
        sync_status.create_status_file(tempdir_path.joinpath(*session))
    # Create some fake statuses
    sync_status.append_status_file(tempdir_path.joinpath(*old), "IdidSomething")
    sync_status.append_status_file(tempdir_path.joinpath(*old2), "IdidSomething")
    sync_status.append_status_file(tempdir_path.joinpath(*one), "IdidSomethingToday")
    sync_status.append_status_file(tempdir_path.joinpath(*two), "IamDoingSomething")

    return tempdir


def test_list_mouse_sessions():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    mousename = "test_mouse"
    # Create some sessions in the tmpdir
    create_fake_sessions(tempdir, "test_mouse_2")
    create_fake_sessions(tempdir, mousename)

    sessions = sn.list_mouse_sessions(mousename, folder_type=Path(tempdir.name))
    assert len(sessions) == 4

    tempdir.cleanup()
