#!/usr/bin/env python
# @File: test_iblrigcore/test_params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, March 7th 2022, 3:34:32 pm
from curses import meta
import json
from pathlib import Path
from typing import List

import pytest

import iblrigcore
from iblrigcore.params import MetaParamFile, ParamFile


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
    assert pars == Bla.template_values

    assert Bla.validate_param_file_keys()
    assert Bla.validate_param_file_values()

    # Test backup creation
    Bla.backup()
    assert Bla.filepath.parent.joinpath(Bla.filename + ".bak").exists()

    # Test write different file and read it back
    pars["MODALITY"] = "OLD"
    Bla.write(pars)
    assert Bla.read() == pars

    # Test update
    upars = Bla.update({"MODALITY": "NEW"})
    # Test read key and output of update method
    assert Bla.read(key="MODALITY") == "NEW"
    assert upars == Bla.read()

    # Test backup file has previois MODALITY value
    with open(Bla.filepath.parent.joinpath(Bla.filename + ".bak"), "r") as f:
        bkpars = json.load(f)
    assert bkpars["MODALITY"] == "OLD"

    # Test delete
    Bla.delete()
    assert Bla.filepath.exists() == False
    assert Bla.filepath_exists == False
    assert ParamFile.filepath[ParamFile.filepath.index(Bla.filepath)].exists() == False
    assert ParamFile.filepath_exists[ParamFile.filepath.index(Bla.filepath)] == False

    # Test restore
    Bla.restore_from_backup()
    assert Bla.read(key="MODALITY") == "NEW"  # Bla.delete will also backup the file
    # Test restore if bk is not there
    bkfile = Bla.filepath.parent.joinpath(Bla.filename + ".bak")
    if bkfile.exists():
        bkfile.unlink()
    pytest.raises(FileNotFoundError, Bla.restore_from_backup)

    # Test update if no file exists
    Bla.delete()
    assert Bla.update({"MODALITY": "BLA"}) is None

    # test init from filepath
    class Bla(ParamFile):
        def __init__(self, *args, **kwargs):
            self.flpth = ParamFile.default_folderpath.joinpath("bla.json")
            self._init_class(filepath=self.flpth)

    # Class init should not create a file
    Bla()
    assert Bla.filename == "bla.json"
    assert Bla.folderpath == ParamFile.default_folderpath
    assert Bla.filepath_exists == False
    Bla.delete()  # should delete nothing


def test_ParamFile_template():
    # Test template
    class Bla(ParamFile, metaclass=MetaParamFile):
        def __init__(self, *args, **kwargs):
            self.flpth = ParamFile.default_folderpath.joinpath("bla.json")
            self.template = {
                "MODALITY": "BLA",
                "EXTRA": 42,
                "EXTRA2": int
            }
            self._init_class(filepath=self.flpth, template=self.template)
            super().__init__(*args, **kwargs)

    bla = Bla()
    template = ParamFile.default_template.copy()
    template.update(bla.template)
    assert Bla.template == template
    Bla.create(populate=False)
    # current params should be the same as Bla.template_values
    assert Bla.read() == Bla.template_values
    assert Bla.validate_param_file_keys()
    assert Bla.validate_param_file_values()
    assert Bla.template_defaults == {'MODALITY': 'BLA', 'EXTRA': 42}
    Bla.delete()

def test_read_update_new_template():
    class Bla(ParamFile, metaclass=MetaParamFile):
        def __init__(self, *args, **kwargs):
            self.flpth = ParamFile.default_folderpath.joinpath("bla.json")
            self.template = {
                "MODALITY": "BLA",
                "EXTRA": 42,
            }
            self._init_class(filepath=self.flpth, template=self.template)
            super().__init__(*args, **kwargs)
    Bla()
    Bla.create(populate=False)
    assert Bla.template_values == Bla.read()
    # Now redifine the class win another extra param in the template
    class Bla(ParamFile, metaclass=MetaParamFile):
        def __init__(self, *args, **kwargs):
            self.flpth = ParamFile.default_folderpath.joinpath("bla.json")
            self.template = {
                "MODALITY": "BLA",
                "EXTRA": 42,
                "EXTRA2": int
            }
            self._init_class(filepath=self.flpth, template=self.template)
            super().__init__(*args, **kwargs)
    Bla()
    # Should stillwork bc on read it should patch the file with the new param
    assert Bla.template_values == Bla.read()
    Bla.delete()


def test_ParamFile_init_error():
    class Bla(ParamFile, metaclass=MetaParamFile):
        def __init__(self, *args, **kwargs):
            self.filepath = ParamFile.default_folderpath.joinpath("bla.json")
            self.filename = "some_file.json"
            self._init_class(filepath=self.filepath, filename=self.filename)
            super().__init__(*args, **kwargs)
    pytest.raises(ValueError, Bla)


def test_ParamFile_multiple():
    # TODO: THIS!
    # Implement acquisition PC that has more than one configuration/param file
    # might need to change the ParamFile class to be able to handle multiple
    # chilren params in the same machine.
    # ParamFile.read_params_file(key="MODALITY") should get the info from a
    # class attribute of the base class that is initialized with the calssmethod\
    # ParamFile.in_use()
    ...
