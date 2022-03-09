#!/usr/bin/env python
# @File: iblrigcore/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, February 28th 2022, 5:11:39 pm
from fileinput import filename
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Union

import iblrigcore

log = logging.getLogger("iblrig")

PARAMS_FILE_PATH = Path().home().joinpath(".iblrigcore_params.json")


class ParamFile:
    """Simple Parameter file interaction class. Creates a class factory that
    doubles as a parent object.

    Returns:
        _type_: _description_
    """

    default_template = {
        "MODALITY": None,
        "DATA_FOLDER_LOCAL": None,  # str
        "DATA_FOLDER_REMOTE": None,  # str
    }
    default_filename = f".iblrigcore_params.json"
    default_folderpath = Path().home().joinpath(".iblrigcore")
    default_filepath = default_folderpath.joinpath(default_filename)

    filename = None  # These could potentially go into the init?
    foderpath = None
    filepath = None
    template = None

    def __init__(self,
        filename: str = None,
        folderpath: Path = None,
        filepath: Path = None,
        template: dict = None,
    ):
        # super(BaseParamFile, cls).__new__(cls)
        super().__init__()
        self.set_file(filename=filename, folderpath=folderpath, filepath=filepath)
        self.set_template(template=template)
        # return cls  # if cls isn't returned the __inint__ is not called

    def init_class
    @classmethod
    def set_file(
        cls, filename: str = None, folderpath: Path = None, filepath: Path = None
    ) -> None:
        """Initializes the ParamFile file args using either a name/folder or a path.
        Set the filepath for the parameter file. determines the folderpath and filename.
        Defaults are used if no input is given.


        Args:
            filename (str, optional): Name of param file. Defaults to None.
            folderpath (Path, optional): folder to save it. Defaults to None.
            filepath (Path, optional): fullpath of paramfile. Defaults to None.

        Raises:
            ValueError: If both filename/folderpath AND filepath are set.
        """
        if filepath and (filename or folderpath):
            raise ValueError(
                "You can specify either filepath or filename/folderpath."
            )
        if filepath:
            filepath = Path(filepath)
            cls.filename = filepath.name
            cls.folderpath = filepath.parent
            cls.filepath = cls.folderpath.joinpath(cls.filename)
        else:
            cls.filename = filename or cls.default_filename
            cls.folderpath = folderpath or cls.default_folderpath
            cls.filepath = Path(cls.folderpath).joinpath(cls.filename)

    @classmethod
    def set_template(cls, template: dict = None) -> None:
        """Initializes the ParamFile arguments (including folderpath, filename and filepath)
        using a given template that will be added to the default_template dictionary.
        Set the template for the parameter file.
        Defaults to the default_template dictionary. Will update it with a templete provided.

        Args:
            template (dict, optional): A template used to generate a new parameter file.
                                        Defaults to None.
        """
        if template is None:
            template = cls.default_template
        else:
            template = {**cls.default_template, **template}
        cls.template = template

    @classmethod
    def write(cls, pars: dict) -> None:
        """Write a full parameter dictionary to the file

        Args:
            pars (dict): dict has to contain all keys from template
        """
        # Check necessary keys are in the parmas you want to write
        assert all([x in pars for x in cls.template]), "Invalid params dict"
        # Create a backup
        cls.backup()
        # Ensure folder exists
        cls.folderpath.mkdir(exist_ok=True)
        # Write the new params truncating old file
        with open(cls.filepath, "w") as f:
            json.dump(pars, f, indent=2)
        return pars

    @classmethod
    def read(cls, key: str = None) -> Union[dict, Any]:
        """Read Parameter file. will return the template if no file is found

        Args:
            key (str, optional): Return only a specific key. Defaults to None.

        Returns:
            Union[dict, Any]: Dict with param values OR value of the requested key
        """
        if not cls.filepath.exists():
            log.debug("Not found: .iblrigcore_params.json creating...")
            return cls.template

        with open(cls.filepath, "r") as f:
            pars = json.load(f)

        if key is None:
            return pars
        else:
            return pars[key]

    @classmethod
    def update(cls, new_pars: dict) -> None:
        """Update Param file with new_pars

        Args:
            new_pars (dict): Partial dict to update the existing one
        """
        log.debug(f"Updating {cls.filename} with {new_pars}")
        # Possible checks for unupdatable params?
        old_pars = cls.read()
        old_pars.update(new_pars)
        cls.write(old_pars)

    @classmethod
    def backup(cls) -> None:
        """Backup Param file, only one version back supported"""
        if cls.filepath.exists():
            log.debug(f"Backing up {cls.filepath}...")
            shutil.move(cls.filepath, cls.filepath.parent.joinpath(cls.filename + ".bak"))
        else:
            log.debug("ParamFile not found, nothing to backup")

    @classmethod
    def delete(cls) -> None:
        """Delete Param file after backing up the old one"""
        cls.backup()
        if cls.filepath.exists():
            log.debug(f"Deleting {cls.filepath}...")
            cls.filepath.unlink()
        else:
            log.debug("ParamFile not found, nothing to delete")

    @classmethod
    def populate(cls):
        """Populate the params dict (user input required)"""
        pars = cls.read()

        for k in pars:
            resp = input(f"{k} [{pars[k]}]: ")
            pars[k] = pars[k] if not resp else resp

        cls.update(pars)


class VideoParamFile(ParamFile):
    # __metaclass__ = BaseParamFile
    def __init__(self, *args, **kwargs):
        # super(VideoParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        # self.template = VideoParamFile.default_template
        self.video_fname = ".videopc_params.json"
        self.video_params = {
            "BODY_CAM_IDX": int,
            "LEFT_CAM_IDX": int,
            "RIGHT_CAM_IDX": int,
        }
        self.set_file(filename=self.video_fname)
        self.set_template(template=self.video_params)


class EphysParamFile(ParamFile):
    # __metaclass__ = BaseParamFile
    def __init__(self, *args, **kwargs) -> None:
        # super(EphysParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        # self.template = EphysParamFile.default_template

    def method():
        print("aaaa")


ephys_fname = ".ephyspc_params.json"
ephys_params = {
    "PROBE_TYPE_00": int,
    "PROBE_TYPE_01": int,
}

print("BaseClass-default\n", ParamFile.default_template)
print("BaseClass\n", ParamFile.template)
print("VideoClass\n", VideoParamFile.template)
print("EphysClass\n", EphysParamFile.template)

# Initiates BaseParamFile class
ParamFile()
# Initiates VideoParamFile class
VideoParamFile()
# Initiates EphysParamFile object
bla = EphysParamFile(filename=ephys_fname, template=ephys_params)

print("---")
print("BaseClass\n", ParamFile.template)
print("VideoClass\n", VideoParamFile.template)
print("EphysClass\n", EphysParamFile.template)
print("EphysInstance\n", bla.template)
