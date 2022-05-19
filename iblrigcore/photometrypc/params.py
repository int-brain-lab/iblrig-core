#!/usr/bin/env python
# @File: photometrypc/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, March 30th 2022, 3:02:25 pm
from typing import List
from iblrigcore.params import ParamFile


class PhotometryParamFile(ParamFile):
    def __init__(self, *args, **kwargs):
        self.flnm = ".photometrypc_params.json"
        self.tmplt = {
            "MODALITY": "photometry",
            "PATCH_CORDS": List,
            "PHOTOMETRY_DEVICE": str,
        }
        self._init_class(filename=self.flnm, template=self.tmplt)
        super().__init__(*args, **kwargs)
