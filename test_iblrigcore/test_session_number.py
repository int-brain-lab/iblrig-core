#!/usr/bin/env python
# @File: test_iblrigcore/test_session_number.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, April 4th 2022, 4:20:40 pm
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import iblrigcore.session_number as sn
import pytest
from iblrigcore import sync_status
from iblrigcore.params import ParamFile
from iblrigcore.photometrypc.params import PhotometryParamFile


def create_fake_sessions(tempdir, mousename):
    PhotometryParamFile.create(populate=False)
    tempdir_path = Path(tempdir.name).joinpath("Subjects")
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
    PhotometryParamFile.delete()

    return tempdir


def test_list_sessions():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    # Create some sessions in the tmpdir
    mousename = "test_mouse"
    create_fake_sessions(tempdir, "test_mouse_2")
    create_fake_sessions(tempdir, mousename)
    sessions = sn.list_sessions(root_folder=Path(tempdir.name))
    assert len(sessions) == 8
    tempdir.cleanup()


def test_list_mouse_sessions():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    mousename = "test_mouse"
    # Create some sessions in the tmpdir
    create_fake_sessions(tempdir, mousename)

    sessions = sn.list_mouse_sessions(Path(tempdir.name), mousename)
    assert len(sessions) == 4
    # Test if the list is sorted
    assert sessions[-1] == Path(tempdir.name).joinpath(
        "Subjects", mousename, datetime.now().date().isoformat(), "002"
    )
    # Test input path has Subjects folder
    sessions2 = sn.list_mouse_sessions(Path(tempdir.name).joinpath("Subjects"), mousename)
    sessions == sessions2
    # Test cannot find Subjects folder
    with pytest.raises(AssertionError) as ae:
        sn.list_mouse_sessions(Path(tempdir.name).joinpath("SomethingWrong"), mousename)
    tempdir.cleanup()


def test_is_session_path():
    assert not sn.is_session_path(Path("/"))
    assert not sn.is_session_path(__file__)
    assert not sn.is_session_path("/some/path/2000-01-01/00a")
    assert not sn.is_session_path("/some/path/2000-01-01/0001")
    assert not sn.is_session_path("/some/path/2000-0101/001")
    assert sn.is_session_path("/some/path/2000-01-01/001")


def test_get_session_number():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    tempdir_remote = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    create_fake_sessions(tempdir, "mouse")
    create_fake_sessions(tempdir_remote, "mouse")
    PhotometryParamFile.create(populate=False)
    pars = ParamFile.read()
    pars["DATA_FOLDER_LOCAL"] = tempdir.name
    pars["DATA_FOLDER_REMOTE"] = tempdir_remote.name
    PhotometryParamFile.write(pars)
    num = sn.get_session_number("mouse")
    assert num == "003"
    # Remove today's sessions
    shutil.rmtree(
        Path(tempdir.name).joinpath("Subjects", "mouse", datetime.now().date().isoformat())
    )
    shutil.rmtree(
        Path(tempdir_remote.name).joinpath("Subjects", "mouse", datetime.now().date().isoformat())
    )
    num2 = sn.get_session_number("mouse")
    assert num2 == "001"
    # Test latest session found is in the future
    Path(tempdir.name).joinpath(
        "Subjects", "mouse", (datetime.now().date() + timedelta(days=1)).isoformat(), "001"
    ).mkdir(parents=True)
    with pytest.raises(ValueError) as ae:
        sn.get_session_number("mouse")
    PhotometryParamFile.delete()
