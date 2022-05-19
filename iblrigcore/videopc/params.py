#!/usr/bin/env python
# @File: videopc/params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, March 30th 2022, 12:10:48 pm
from iblrigcore.params import ParamFile


class VideoParamFile(ParamFile):
    def __init__(self, *args, **kwargs):
        self.video_fname = ".videopc_params.json"
        self.video_template = {
            "MODALITY": "video",
            "BODY_CAM_IDX": int,
            "LEFT_CAM_IDX": int,
            "RIGHT_CAM_IDX": int,
        }
        self._init_class(filename=self.video_fname, template=self.video_template)
        # super(VideoParamFile, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
