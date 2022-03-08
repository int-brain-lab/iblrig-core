#!/usr/bin/env python
# @File: test_iblrigcore/test_params.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, March 7th 2022, 3:34:32 pm
import iblrigcore.params as params
from iblrigcore.params import ParamFile


def test_param_file():
    ParamFile.delete()
    assert ParamFile.path.exists() == False
    assert ParamFile.path.parent.joinpath
