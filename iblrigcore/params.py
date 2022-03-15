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


class ParamFile:
    """Simple Parameter file interaction class. Creates a class factory that
    doubles as a parent object.

    Returns:
        _type_: _description_
    """

    default_template = {
        "MODALITY": str,
        "DATA_FOLDER_LOCAL": str,
        "DATA_FOLDER_REMOTE": str,
    }
    default_filename = f".iblrigcore_params.json"
    default_folderpath = Path().home().joinpath(".iblrigcore")
    default_filepath = default_folderpath.joinpath(default_filename)

    filename = None  # These could potentially go into the init?
    foderpath = None
    filepath = None
    template = None

    def __init__(
        self,
        filename: str = None,
        folderpath: Path = None,
        filepath: Path = None,
        template: dict = None,
    ):
        super().__init__()
        ParamFile._set_base_attributes()

    def __init_subclass__(
        cls,
        filename: str = None,
        folderpath: Path = None,
        filepath: Path = None,
        template: dict = None,
    ):
        """Guarantees the template filename and filepath class attributes are populated with the
        default values on subclassing. All logic of the Base class uses these attributes, so if user does not
        call the init_class method the subclass will still work."""
        super().__init_subclass__()
        cls.init_class(
            filename=filename, folderpath=folderpath, filepath=filepath, template=template
        )
        ParamFile._set_base_attributes()

    @classmethod
    def init_class(
        cls,
        filename: str = None,
        folderpath: Path = None,
        filepath: Path = None,
        template: dict = None,
    ):
        """Initializes the class file args using either a name/folder or a path.
        Set the filepath for the parameter file. determines the folderpath and filename.
        Defaults are used if no input is given.


        Args:
            filename (str, optional): Name of param file. Defaults to None.
            folderpath (Path, optional): folder to save it. Defaults to None.
            filepath (Path, optional): fullpath of paramfile. Defaults to None.

        Raises:
            ValueError: If both filename/folderpath AND filepath are set.
        """
        cls.set_file(filename=filename, folderpath=folderpath, filepath=filepath)
        cls.set_template(template=template)

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
            raise ValueError("You can specify either filepath or filename/folderpath.")
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
        if not isinstance(cls.template, dict):
            cls.template = {}
        if template is None:
            template = cls.default_template
        else:
            template = {**cls.default_template, **template}
        cls.template.update(template)

    @classmethod
    def write(cls, pars: dict) -> None:
        """Write a full parameter dictionary to the file.
        Compares keys to cls.template, backs up previous param file if exists
        Writes new param file to cls.filepath

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
        if isinstance(cls.filepath, list):
            ...

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
    def _set_base_attributes(cls) -> None:
        """Finds the existing filepaths and templates of any ParamFile children.
        Sets the base class attributes based on the existing subclass attributes.
        """
        fpaths = []
        templates = []
        for subc in cls.__subclasses__():
            fpaths.append(subc.__dict__.get("filepath", None))
            templates.append(subc.__dict__.get("template", None))

        ParamFile.filepath = fpaths
        ParamFile.filename = [x.name for x in fpaths]
        ParamFile.folderpath = [x.parent for x in fpaths]
        ParamFile.template = templates

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
    # __metaclass__ = ParamFile
    def __init__(self, *args, **kwargs):
        self.video_fname = ".videopc_params.json"
        self.video_params = {
            "BODY_CAM_IDX": int,
            "LEFT_CAM_IDX": int,
            "RIGHT_CAM_IDX": int,
        }
        self.init_class(filename=self.video_fname, template=self.video_params)
        # super(VideoParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)


class EphysParamFile(ParamFile):
    # __metaclass__ = ParamFile
    def __init__(self, *args, **kwargs) -> None:
        self.ephys_fname = ".ephyspc_params.json"
        self.ephys_params = {
            "PROBE_TYPE_00": int,
            "PROBE_TYPE_01": int,
        }
        self.init_class(filename=self.ephys_fname, template=self.ephys_params)
        # super(EphysParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

ParamFile()
VideoParamFile()
EphysParamFile()



# print("BaseClass-default\n", ParamFile.default_template)
# print("BaseClass\n", ParamFile.template)
# # subclassed classes should have the default template populated as per __init_subclass__
# print("VideoClass\n", VideoParamFile.template)
# print("EphysClass\n", EphysParamFile.template)

# # Initiates ParamFile class
# ParamFile()
# # Initiates VideoParamFile class
# VideoParamFile()
# # Initiates EphysParamFile object and instanciates it
# bla = EphysParamFile()
# ble = VideoParamFile()

# print("---")
# print("BaseClass\n", ParamFile.template)
# print("VideoClass\n", VideoParamFile.template)
# print("EphysClass\n", EphysParamFile.template)
# print("EphysInstance\n", bla.template)
# print("VideoInstance\n", ble.template)

# # Multiple inheritance gets messy but can return a cumulative template of all parent classes :)
# class VideoEphysParamFile(EphysParamFile, VideoParamFile):
#     __metaclass__ = ParamFile
#     ...