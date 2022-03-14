#!/usr/bin/env python
# @File: iblrigcore/start_acquisition.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Monday, February 28th 2022, 4:49:19 pm
"""_summary_: Implements the startup acquisition logic with local server synchronization."""


def start_acquisition(mouse: str):
    """_summary_

    Args:
        mouse (str): _description_
    """
    print(f"Starting acquisition for mouse {mouse}")
    # Load local parameter file TODO: add modality to the parameter file
    # Check the remote_folder for a session name given the mouse inpout and the current date
    # if no sessions exist today session_number == 001
        # Create remote folder
        # Create session_status.csv in the remote_folder
        # Add a row to the session_status.csv with the following info:
        # ["Timestamp", "ComputerName", "Caller", "Modality", "Action"]