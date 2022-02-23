#!/usr/bin/env python
# @File: test_iblrigcore/test_version.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, February 23rd 2022, 3:22:39 pm
def test_version():
    import iblrigcore
    assert iblrigcore.__version__