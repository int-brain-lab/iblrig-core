#!/usr/bin/env python
# @File: test_iblrigcore/test_params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, March 7th 2022, 3:34:32 pm
import json
from pathlib import Path
from typing import Any, List, Union

import iblrigcore.params as params
from iblrigcore.params import ParamFile


def test_ParamFile_base_class_initialization():
    """
    """
    default_template = {
        "MODALITY": str,
        "DATA_FOLDER_LOCAL": str,
        "DATA_FOLDER_REMOTE": str,
    }
    default_filename = f".iblrigcore_params.json"
    default_folderpath = Path().home().joinpath(".iblrigcore")
    default_filepath = default_folderpath.joinpath(default_filename)

    _classname: List[str] = []
    _filename: List[str] = []
    _folderpath: List[Path] = []
    _template: List[dict] = []
    _filepath: List[Path] = []
    _filepath_exists: List[bool] = []

    assert ParamFile.default_template == default_template
    assert ParamFile.default_filename == default_filename
    assert ParamFile.default_folderpath == default_folderpath
    assert ParamFile.default_filepath == default_filepath
    assert (
        ParamFile.classname
        == ParamFile.filename
        == ParamFile.folderpath
        == ParamFile.template
        == ParamFile.filepath
        == ParamFile.filepath_exists
        == []
    )


def test_ParamFile_IO():
    """Tests ParanFile subclass IO behavior
    Base class methods Fails to do IO for now"""
    class Bla(ParamFile):
        ...

    Bla()

    Bla.new_from_template()
    assert Bla.filepath_exists == True
    # Making and instance of ParamFile should change the BaseClass attributes:
    assert Bla.filepath == ParamFile.filepath
    assert Bla.folderpath == ParamFile.folderpath
    assert Bla.template == ParamFile.template
    assert Bla.filename == ParamFile.filename
    assert Bla.filepath_exists == ParamFile.filepath_exists

    # Read back the file you just created and compare the content to the template
    pars = Bla.read()
    assert pars == {k: str(v) for k, v in Bla.template.items()}

    assert Bla.validate()
    assert Bla.validate_param_values()

    # Test backup creation
    Bla.backup()
    assert Bla.filepath.parent.joinpath(Bla.filename + ".bak").exists()

    # Test write different file and read it back
    pars["MODALITY"] = "MOVIE"
    Bla.write(pars)
    assert Bla.read() == pars

    # Test update
    Bla.update({"MODALITY": "BLA"})
    # Test read key and output of update method
    assert Bla.read(key="MODALITY") == "BLA"

    # Test backup file has previois MODALITY value
    with open(Bla.filepath.parent.joinpath(Bla.filename + ".bak"), 'r') as f:
        bkpars = json.load(f)
    assert bkpars["MODALITY"] == "MOVIE"

    # Test delete
    Bla.delete()
    assert Bla.filepath.exists() == False
    assert Bla.filepath_exists == False
    assert ParamFile.filepath.exists() == False
    assert ParamFile.filepath_exists == False






def test_param_file_delete():
    ParamFile.delete()
    assert ParamFile.filepath.exists() == False
