#!/usr/bin/env python
# @File: videopc/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, March 30th 2022, 12:10:48 pm
import pathlib
from iblrigcore.params import ParamFile
import iblrigcore  # noqa
import logging
from pathlib import Path


log = logging.getLogger("iblrig")


class BehaviorParamFile(ParamFile):
    """For now requires iblrig to be installed
    TODO: migrate all path habndling funcs to iblrigcore/paths.py"""

    def __init__(self, *args, **kwargs) -> None:
        self.behavior_fname = ".iblrig_params.json"
        self.behavior_folderpath = self._get_folderpath()
        self.behavior_template = {
            "NAME": str,
            "IBLRIG_VERSION": str,
            "COM_BPOD": str,
            "COM_ROTARY_ENCODER": str,
            "COM_F2TTL": str,
            "F2TTL_HW_VERSION": float,
            "F2TTL_DARK_THRESH": float,
            "F2TTL_LIGHT_THRESH": float,
            "F2TTL_CALIBRATION_DATE": str,
            "SCREEN_FREQ_TARGET": int,  # (Hz)
            "SCREEN_FREQ_TEST_STATUS": str,
            "SCREEN_FREQ_TEST_DATE": str,
            "SCREEN_LUX_VALUE": float,
            "SCREEN_LUX_DATE": str,
            "WATER_CALIBRATION_RANGE": List[float],  # [min, max]
            "WATER_CALIBRATION_OPEN_TIMES": List[float],  # [float, float, ...]
            "WATER_CALIBRATION_WEIGHT_PERDROP": List[float],  # [float, float, ...]
            "WATER_CALIBRATION_DATE": str,
            "BPOD_TTL_TEST_STATUS": str,
            "BPOD_TTL_TEST_DATE": str,
            "DATA_FOLDER_LOCAL": str,
            "DATA_FOLDER_REMOTE": str,
            "DISPLAY_IDX": int,
        }
        self._init_class(
            filename=self.behavior_fname,
            folderpath=self.behavior_folderpath,
            template=self.behavior_template,
        )
        # super(EphysParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def _get_folderpath(self) -> Path:
        try:
            import iblrig.path_helper as ph

            return Path(ph.get_iblrig_params_folder())
        except ModuleNotFoundError:
            log.debug("iblrig not installed, falling back to default params folder")
            import platform

            if platform.uname().node == "pfc":
                return Path("/home/nico/Projects/IBL/int-brain-lab/iblrig_params")
            else:
                return BehaviorParamFile.default_folderpath


# TODO: implement default values and auto updatable values on read/write
