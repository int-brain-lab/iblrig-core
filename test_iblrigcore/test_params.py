#!/usr/bin/env python
# @File: test_iblrigcore/test_params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, March 7th 2022, 3:34:32 pm
import iblrigcore.params as params
from iblrigcore.params import EphysParamFile, ParamFile, VideoParamFile


def test_param_file_delete():
    ParamFile.delete()
    assert ParamFile.filepath.exists() == False
    VideoParamFile.delete()
    assert VideoParamFile.filepath.exists() == False
    EphysParamFile.delete()
    assert EphysParamFile.filepath.exists() == False

def test_param_file_create():
    ...