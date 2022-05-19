#!/usr/bin/env python
# @File: test_iblrigcore/test_sync_status.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Thursday, February 24th 2022, 11:46:54 am
import tempfile
from pathlib import Path

from iblrigcore import sync_status
from iblrigcore.sync_status import caller
from iblrigcore.photometrypc.params import PhotometryParamFile


#FIXME: import params and create then delete at end of test module
def test_timestamp():
    assert isinstance(sync_status.timestamp(), str)


def test_computer_name():
    assert isinstance(sync_status.computer_name(), str)


def test_create_status_file():
    PhotometryParamFile.create(populate=False)
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    sync_status.create_status_file(tempdir.name)
    assert Path(tempdir.name).joinpath("session_status.csv").exists()
    # Test create status file when it already exists
    sync_status.create_status_file(tempdir.name)  # Nothing happens
    tempdir.cleanup()
    PhotometryParamFile.delete()


def test_load_status_file():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    PhotometryParamFile.create(populate=False)
    sync_status.create_status_file(tempdir.name)
    status_file = sync_status.load_status_file(tempdir.name)
    assert status_file is not None
    header = ["Timestamp", "ComputerName", "Caller", "Modality", "Action"]
    assert header in status_file
    status_file = sync_status.load_status_file(tempdir.name, header=False)
    assert header not in status_file
    tempdir.cleanup()
    # Test load status file when it does not exist
    status_file = sync_status.load_status_file(tempdir.name)
    assert not status_file
    PhotometryParamFile.delete()


def test_caller():
    fullpath = Path(__file__)
    modulename = fullpath.name.split(".")[0]
    packagename = fullpath.parent.name
    out = caller(1)
    assert out == ".".join([packagename, modulename, "test_caller"])


def test_caller_one_level_deeper():
    fullpath = Path(__file__)
    modulename = fullpath.name.split(".")[0]
    packagename = fullpath.parent.name

    def fake_row(var):
        return caller(var)

    out = fake_row(2)
    assert out == ".".join([packagename, modulename, "test_caller_one_level_deeper"])


def test_append_status_file():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    PhotometryParamFile.create(populate=False)
    sync_status.create_status_file(tempdir.name)
    sync_status.append_status_file(tempdir.name, "IdidSomething")
    sf_data = sync_status.load_status_file(tempdir.name)
    assert sf_data[-1][-1] == "IdidSomething"
    tempdir.cleanup()
    # status file missing test
    sync_status.append_status_file(tempdir.name, "IdidSomething")
    sf_data = sync_status.load_status_file(tempdir.name)
    assert not sf_data
    PhotometryParamFile.delete()
