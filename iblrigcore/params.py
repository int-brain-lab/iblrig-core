# PLACEHOLDER, MOST LIKELY SAFE TO OVERWRITE

import json
import logging
from pathlib import Path
from typing import Any, Union

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