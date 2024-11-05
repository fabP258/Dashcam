# Dashcam
SW running the data recording device

## Getting started

### Prerequisites

This application relies on the **Picamera2** library for dealing with the cameras. Before setting up the virtual environment it is necessary to have it installed system wide. If the library is not installed please follow the instructions here: [Picamera2](https://github.com/raspberrypi/picamera2)

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

## Remarks

It is known when playing the recored video with e.g. VLC they seem to be laggy. To avoid this a simple post-processing can be run using `ffmpeg` specifying the frame rate can be applied

`ffmpeg -r 25 -i video.h264 video.mkv`

