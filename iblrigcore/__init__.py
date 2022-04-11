__version__ = "0.0.1"
#!/usr/bin/env python
# @File: iblrigcore/__init__.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, February 23rd 2022, 10:45:20 am
"""iblrig core classes and functions
# Configuration
- Parameter files and data IO are defined here. (params.py)
Default parameter configuration:
{
    MODALITY: str,
    DATA_FOLDER_LOCAL: str,
    DATA_FOLDER_REMOTE: str
}

# Acquisition:
(All acquisition startup/shutdown logic is based on a user provided subject name)

@acquisition_start:
- Determine session name: <subject>/<date>/<number> from local/remote data folder
- Create or attach to a sync_status.csv file in the remote data folder
- Log actions performed by the PC to sync_status.csv
- Create a local session metadata file in DATA_FOLDER_LOCAL / raw_<MODALITY>_data / metadata.json
- Launch the acquisition logic

@acquisition_stop:
- Raw data QC anv validation
- Cleanup

# Transfer:
- Transfer raw acquisition data to local server.
    - Check for session_status.csv and create if missing.
    - Log transfer_status as started
    - Validate data files on remote server.
    - Log transfer_status as ended/validated
    - Check create a raw_session.flag to initiate the pipeline

# Cleanup:
(rigs/computers should have safe maintenance / cleanup logic)
"""
import iblrigcore.logging_  # noqa

# Import all bilrigcore params classes to register them in the ParamFile class
from iblrigcore.params import ParamFile  # noqa
from iblrigcore.videopc.params import VideoParamFile
from iblrigcore.ephyspc.params import EphysParamFile
from iblrigcore.photometrypc.params import PhotometryParamFile
# from iblrigcore.behaviorpc.params import BehaviorParamFile

# Initialize all classes
ParamFile()
VideoParamFile()
EphysParamFile()
PhotometryParamFile()
# BehaviorParamFile()