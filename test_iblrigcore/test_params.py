#!/usr/bin/env python
# @File: test_iblrigcore/test_params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, March 7th 2022, 3:34:32 pm
import json
from pathlib import Path
from typing import List

import iblrigcore
from iblrigcore.params import ParamFile


def test_ParamFile_base_class_initialization():
    """ """
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

    # Test defaults
    assert ParamFile.default_template == default_template
    assert ParamFile.default_filename == default_filename
    assert ParamFile.default_folderpath == default_folderpath
    assert ParamFile.default_filepath == default_filepath


def test_singletons__init__():

    classes = [
        v
        for v in iblrigcore.__dict__.values()
        if isinstance(v, iblrigcore.params.MetaParamFile) and v.__name__ != "ParamFile"
    ]

    # Test attributes XXX: add tests here for new modalities param files
    assert ParamFile.classname == [x.__name__ for x in classes]
    assert ParamFile.filename == [x.filename for x in classes]
    assert ParamFile.folderpath == [x.folderpath for x in classes]
    assert ParamFile.template == [x.template for x in classes]
    assert ParamFile.filepath == [x.filepath for x in classes]
    assert ParamFile.filepath_exists == [x.filepath_exists for x in classes]


def test_ParamFile_IO():
    """Tests ParamFile subclass IO behavior
    Base class methods Fails to do IO for now"""

    class Bla(ParamFile):
        ...

    Bla()

    Bla.create(populate=False)
    assert Bla.filepath_exists == True
    # Making and instance of ParamFile should change the BaseClass attributes:
    assert Bla.filepath in ParamFile.filepath
    assert Bla.folderpath in ParamFile.folderpath
    assert Bla.template in ParamFile.template
    assert Bla.filename in ParamFile.filename
    assert Bla.filepath_exists == ParamFile.filepath_exists[ParamFile.filepath.index(Bla.filepath)]

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
    with open(Bla.filepath.parent.joinpath(Bla.filename + ".bak"), "r") as f:
        bkpars = json.load(f)
    assert bkpars["MODALITY"] == "MOVIE"

    # Test delete
    Bla.delete()
    assert Bla.filepath.exists() == False
    assert Bla.filepath_exists == False
    assert ParamFile.filepath[ParamFile.filepath.index(Bla.filepath)].exists() == False
    assert ParamFile.filepath_exists[ParamFile.filepath.index(Bla.filepath)] == False

    # Test restore
    Bla.restore_from_backup()
    Bla.read(key="MODALITY") == "MOVIE"

    # Test update if no file exists
    Bla.delete()
    Bla.update({"MODALITY": "BLA"})


    # test init from filepath
    class Bla(ParamFile):
        def __init__(self, *args, **kwargs):
            self.flpth = ParamFile.default_folderpath.joinpath("bla.json")
            self._init_class(filepath=self.flpth)

    bla = Bla()
    bla.delete()
def test_ParamFile_multiple():
    ...
