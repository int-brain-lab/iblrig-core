# iblrig-core

This repository is used in conjunction with [iblrig](https://github.com/int-brain-lab/iblrig). The intent is to only utilize the python standard libraries as much as possible, keeping the number of dependencies to a minimum. Additional requirements **may** eventually include `numpy` and `pandas` at some point in the future.

This Python package implements all file transfer and system logic for the various rig configurations. This includes behavior, ephys, video, mesoscope, and others.

Current requirement is for python version is 3.7+, this is for iblrig behavior PC compatibility.

---
### Installation and upgrade instruction
- ensure that you are the correct virtual environment, i.e. something like: 
  - `conda activate iblrig`
- install or upgrade through pip: 
  - `pip install iblrig-core` 
  - `pip install --upgrade iblrig-core`

---
### Development
Tests and flake 8 run on push or pull requests (PR) to the develop branch.

Automatic PyPI release on push of tag with a "v*" prefix.

Development requirements:
- flake8
- black
- pytest

This repo is using gitflow and semantic versioning conventions. Click on the following links for more information on [gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) or [semantic versioning](https://semver.org/).