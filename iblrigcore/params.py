#!/usr/bin/env python
# @File: iblrigcore/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, February 28th 2022, 5:11:39 pm
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Union

import iblrigcore

log = logging.getLogger("iblrig")

PARAMS_FILE_PATH = Path().home().joinpath(".iblrigcore_params.json")


class ParamFile:
    """Simple Parameter file interaction class

    Returns:
        _type_: _description_
    """
    default_params = {
        "MODALITY": None,
        "DATA_FOLDER_LOCAL": None,  # str
        "DATA_FOLDER_REMOTE": None,  # str
    }
    default_filename = ".iblrigcore_params.json"
    default_folderpath = Path().home().joinpath(".iblrigcore")
    default_filepath = default_folderpath.joinpath(default_filename)

    filename = None
    foderpath = None
    filepath = None

    @classmethod
    def set_filepath(cls, path: Path = None) -> None:
        if path is None:
            path = cls.default_filepath
        path = Path(path)
        cls.filename = path.name
        cls.folderpath = path.parent
        cls.filepath = cls.folderpath.joinpath(cls.filename)

    @classmethod
    def write(cls, pars: dict) -> None:
        # Check necessary keys are in the parmas you want to write
        assert all([x in pars for x in cls.default_params]), "Invalid params dict"
        # Create a backup
        ParamFile.backup()
        # Ensure folder exists
        cls.folderpath.mkdir(exist_ok=True)
        # Write the new params truncating old file
        with open(cls.filepath, "w") as f:
            json.dump(pars, f)

    @classmethod
    def read(cls, key: str = None) -> Union[dict, Any]:
        """Read Param file, will create a default parameter file if not found.

        Args:
            key (str, optional): Return only a specific key. Defaults to None.

        Returns:
            Union[dict, Any]: Dict with param values OR value of the requested key
        """
        if not cls.filepath.exists():
            log.debug("Not found: .iblrigcore_params.json creating...")
            cls.write(cls.default_params)

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
        log.debug(f"Updating .iblrigcore_params.json with {new_pars}")
        # Possible checks for unupdatable params?
        # old_pars = ParamFile.read()
        # old_pars.update(new_pars)
        cls.write(cls.read().update(new_pars))
        pass

    @classmethod
    def backup(cls) -> None:
        """Backup Param file, only one version back supported
        """
        if cls.filepath.exists():
            shutil.move(
                cls.filepath, cls.filepath.parent.joinpath(".iblrigcore_params.json.bak")
            )
        else:
            log.debug("ParamFile not found, nothing to backup")

    @classmethod
    def delete(cls) -> None:
        """Delete Param file after backing up the old one
        """
        cls.backup()
        cls.filepath.unlink()

ParamFile.set_filepath()


class VideoParamFile(ParamFile):
    """Behavior Parameter file interaction class"""
    @classmethod
    def create_videopc_params(cls):
        # Default name and location OK
        cls.set_filepath()
        default_params = cls.default_params
        vidopc_params = {
            "BODY_CAM_IDX": None,
            "LEFT_CAM_IDX": None,
            "RIGHT_CAM_IDX": None,
        }
        # Populate with values (ask user if not found) TODO: add populate method!!
        # Update default params with vidopc_params
        cls.write(cls.default_params)
        cls.update
        print("create")


def create_default_local_params() -> None:
    ParamFile.write(ParamFile.default_params)
    return


def create_local_params(params: dict) -> None:
    if ParamFile.path.exists():
        raise Exception("Params file already exists")
    else:

        ParamFile.write(
            {
                "MODALITY": modality,
                "LOCAL_DATA_FOLDER": local_data_folder,
                "REMOTE_DATA_FOLDER": remote_data_folder,
            }
        )
    return
