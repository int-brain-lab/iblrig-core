#!/usr/bin/env python
# @File: test_iblrigcore/test_sync_status.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Thursday, February 24th 2022, 11:46:54 am
import tempfile
from pathlib import Path

import pytest
from iblrigcore import sync_status
from iblrigcore.sync_status import caller_old, caller
from pytest import skip


def test_timestamp():
    assert isinstance(sync_status.timestamp(), str)


def test_computer_name():
    assert isinstance(sync_status.computer_name(), str)


def test_create_status_file():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    sync_status.create_status_file(tempdir.name)
    assert Path(tempdir.name).joinpath("session_status.csv").exists()
    tempdir.cleanup()


def test_load_status_file():
    tempdir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
    sync_status.create_status_file(tempdir.name)
    status_file = sync_status.load_status_file(tempdir.name)
    assert status_file is not None
    header = ["Timestamp", "ComputerName", "Caller", "Modality", "Action"]
    assert header in status_file
    status_file = sync_status.load_status_file(tempdir.name, header=False)
    assert header not in status_file
    tempdir.cleanup()


@pytest.mark.skip(reason="old caller function")
def test_caller_old():
    fullpath = Path(__file__)
    out = caller_old(True)
    assert out == str(fullpath) + "/" + "test_caller"
    out = caller_old(False)
    assert out == str(fullpath.name) + "/" + "test_caller"


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
    sync_status.create_status_file(tempdir.name)
    sync_status.append_status_file(tempdir.name, "IdidSomething")
    sf_data = sync_status.load_status_file(tempdir.name)
    assert sf_data[-1][-1] == "IdidSomething"
    tempdir.cleanup()
