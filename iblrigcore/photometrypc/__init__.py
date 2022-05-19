#!/usr/bin/env python
# @File: videopc/__init__.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, February 23rd 2022, 4:20:19 pm
"""PhotometryPC required steps:
Params file with mapping between patchcords and number of expected photometry fibers/column names.

@acquisition_start:
- Attribute fibers to subjects to be able to split the table after acquisition.
- Define and create raw acquisition session data folder.
- Create acquisition settings/metadata file, add to data folder.
@acquisition_stop:
- Create mouse/date/number/raw_photometry_data folder(s) according to acquisition settings.
- Split the photomentry raw table in the respective files and save them into the created folders.
@transfer:
- Transfer from Photometry PC to local server
- TODO: decide if we want to save the raw photometry unsplitted session on local server and how.
- Create raw_session.flag to initializa pipeline.

Alyx/Pipeline Requirements:
- New dataset types should exist on Alyx:
    - daq sync file for behavior rig
    - raw? and splitted photometry datasets
- Local server preproc pipeline should:
    1. Register session(s)and initialte transfer of raw session data
    2. Extract trial table using raw pybpod data
        2a. Synchronize bpod data to daq clock.
    3. Extract photometry data
        3a. Synchronize photometry data timestamps to daq clock.
    6. QC extracted photometry data
"""
