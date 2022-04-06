#!/usr/bin/env python
# @File: iblrigcore/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, February 28th 2022, 5:11:39 pm
import json
import logging
import shutil
from pathlib import Path
from typing import Any, List, Union, List

import iblrigcore  # noqa

log = logging.getLogger("iblrig")


class MetaParamFile(type):
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

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post_init__(cls, *args, **kwargs)
        return obj

    @staticmethod
    def _get_value(clsvar):
        if len(clsvar) == 1:
            return clsvar[0]
        else:
            return clsvar

    @staticmethod
    def _parse_value(value):
        if not isinstance(value, list):
            return [value]
        else:
            return value

    @property
    def filepath(cls):
        return cls._get_value(cls._filepath)

    @filepath.setter
    def filepath(cls, value):
        cls._filepath = cls._parse_value(value)

    @property
    def filename(cls):
        return cls._get_value(cls._filename)

    @filename.setter
    def filename(cls, value):
        cls._filename = cls._parse_value(value)

    @property
    def folderpath(cls):
        return cls._get_value(cls._folderpath)

    @folderpath.setter
    def folderpath(cls, value):
        cls._folderpath = cls._parse_value(value)

    @property
    def filepath_exists(cls):
        return cls._get_value([x.exists() for x in cls._filepath])

    @filepath_exists.setter
    def filepath_exists(cls, value):
        cls._filepath_exists = cls._parse_value(value)

    @property
    def template(cls):
        return cls._get_value(cls._template)

    @template.setter
    def template(cls, value):
        cls._template = cls._parse_value(value)

    @property
    def classname(cls):
        return cls._get_value(cls._classname)

    @classname.setter
    def classname(cls, value):
        cls._classname = cls._parse_value(value)

    def check_base_class(cls):
        return cls.__name__ == "ParamFile"


class ParamFile(object, metaclass=MetaParamFile):
    """Simple Parameter file interaction class. Creates a class factory that
    doubles as a parent object.

    Returns:
        _type_: _description_
    """

    def __init__(self):
        super().__init__()
        ParamFile._update_base_attributes()
        self.someattrib = 42  # only accessible to the instances

    @classmethod
    def __post_init__(cls, *args, **kwargs):
        # cls._init_class(**kwargs)
        # # super(VideoParamFile, self).__init__(*args, **kwargs)
        # super().__init__(*args, **kwargs)
        pass

    @classmethod
    def __init_subclass__(
        cls,
        filename: str = None,
        folderpath: Path = None,
        filepath: Path = None,
        template: dict = None,
    ):
        """Guarantees the template filename and filepath class attributes are populated with the
        default values on subclassing. All logic of the Base class uses these attributes so,
        if user does not call the init_class method the subclass will still work."""
        super().__init_subclass__()
        cls._init_class(
            filename=filename, folderpath=folderpath, filepath=filepath, template=template
        )

    @classmethod
    def _update_base_attributes(cls) -> None:
        """Finds the existing filepaths and templates of any ParamFile children.
        Sets the base class attributes based on the existing subclass attributes.
        """
        # TODO: call _update_base_attributes on __del__ to remove deleted children
        fpaths = []
        templates = []
        classnames = []
        for subc in ParamFile.__subclasses__():
            fpaths.extend(subc.__dict__.get("_filepath", None))
            templates.extend(subc.__dict__.get("_template", None))
            classnames.append(subc.__name__)
        ParamFile.filepath = fpaths
        ParamFile.filepath_exists = [x.exists() for x in fpaths]
        ParamFile.filename = [x.name for x in fpaths]
        ParamFile.folderpath = [x.parent for x in fpaths]
        ParamFile.template = templates
        ParamFile._classname = classnames

    @classmethod
    def _init_class(
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
        cls._set_file(filename=filename, folderpath=folderpath, filepath=filepath)
        cls._set_template(template=template)

    @classmethod
    def _set_file(
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
            cls.filepath_exists = cls.filepath.exists()
        else:
            cls.filename = filename or cls.default_filename
            cls.folderpath = folderpath or cls.default_folderpath
            cls.filepath = Path(cls.folderpath).joinpath(cls.filename)
            cls.filepath_exists = cls.filepath.exists()

    @classmethod
    def _set_template(cls, template: dict = None) -> None:
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

        cls._classname = cls.__name__

    @staticmethod
    def read_params_file(key: str = "") -> Union[dict, List[dict]]:
        """Reads all the parameter files that exist on the system.
        NB: there should only be one file to read from on any given acquisition computer.

        Returns:
            Union[dict, List[dict]]: Dict with param values OR list with dicts.
        """
        subclasses = list(ParamFile.__subclasses__())
        pfiles = [p.read() for p in subclasses]
        assert len(subclasses) == len(pfiles), "Not all pars files read"
        valid_params = {x.__name__: y for x, y in zip(subclasses, pfiles) if y is not None}
        if not valid_params:
            log.warning("No valid ParamFiles found.")
            return
        elif len(valid_params) == 1:
            log.info(f"Returning {[k for k in valid_params][0]} params.")
            valid_params = valid_params[list(valid_params.keys())[0]]
        else:
            log.info(f"Returning {[k for k in valid_params]} all ParamFiles.")
        return valid_params[key] if key else valid_params

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
        """Read Parameter file.
        Base class behavior: Will return the param file if only one param file is found
            among allchildren classes
        Subclass behavior:Will return

        Args:
            key (str, optional): Return only a specific key. Defaults to None.

        Returns:
            Union[dict, Any]: Dict with param values OR value of the requested key
        """
        if cls.check_base_class():
            return cls.read_params_file(key=key)

        if not cls.filepath.exists():
            log.debug(f"Not found: {cls.filepath} does not exist")
            return

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
        if not cls.filepath_exists:
            log.error(f"Not found: {cls.filepath} does not exist")
            return

        log.debug(f"Updating {cls.filename} with {new_pars}")
        # Possible checks for unupdatable params?
        old_pars = cls.read()
        # All keys of new_pars should exist in old_pars
        for key in new_pars:
            assert key in old_pars, "Trying to update a non-existing key"

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
    def restore_from_backup(cls) -> None:
        """Restores the original file from the backup"""
        backup_filepath = cls.filepath.parent.joinpath(cls.filename + ".bak")
        if backup_filepath.exists():
            log.debug(f"Restoring {cls.filepath} from backup")
            shutil.move(backup_filepath, cls.filepath)
        else:
            log.debug("Cannot restore, backup file not found")

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

    @classmethod
    def new_from_template(cls) -> None:
        """Allows you to create a new param file in the folderpath."""
        cls.folderpath.mkdir(exist_ok=True)

        # Preserve the old file
        cls.backup()
        filepath = cls.filepath
        template = {k: str(v) for k, v in cls.template.items()}
        cls.write(template)
        return filepath

    @classmethod
    def create(cls, populate: bool = True) -> None:
        """creates a new param file and populates it
        If populate is False then the file is created with the default values of the template

        Args:
            populate (bool, optional): Ask user values of each parameter. Defaults to True.
        """
        cls.new_from_template()
        if populate:
            cls.populate()

    @classmethod
    def validate(cls) -> bool:
        """Validate the current param file against the template
        Returns True if the current param file matches the template
        """
        template = {k: str(v) for k, v in cls.template.items()}
        current = cls.read()
        return template == current

    @classmethod
    def validate_param_values(cls) -> bool:
        """Validate the types of the current param file against the template
        Returns True if the current param file matches the template
        """
        current = cls.read()
        return all([isinstance(current[k], cls.template[k]) for k in cls.template])

# TODO: Create decorator to avoid running BaseClass methods that require initialization
# https://stackoverflow.com/questions/25828864/catch-before-after-function-call-events-for-all-functions-in-class
