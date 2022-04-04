#!/usr/bin/env python
# @File: videopc/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, March 30th 2022, 12:10:48 pm
from iblrigcore.params import ParamFile


class EphysParamFile(ParamFile):
    def __init__(self, *args, **kwargs) -> None:
        self.filename = ".ephyspc_params.json"
        self.template = {
            "MODALITY": "ephys",
            "PROBE_TYPE_00": int,
            "PROBE_TYPE_01": int,
        }
        self._init_class(filename=self.filename, template=self.template)
        # super(EphysParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
