# Dashcam
SW running the data recording device

## Getting started

### Setup venv

* Setup a python virtual environment and use the system python packages:

`sudo apt install python3-virtualenv`

`python3 -m venv --system-site-packages env`

* Activate virtual environment:
`source env/bin/activate`

*Picamera2* should be available from the system packages.

### Install package

`python3 setup.py sdist bdist_wheel`

`pip install -e .`

