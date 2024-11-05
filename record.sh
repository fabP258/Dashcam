#!/bin/bash

VENV_PATH="./env"

SCRIPT_PATH="./src/recorder/main.py"

source "$VENV_PATH/bin/activate"

python "$SCRIPT_PATH"

deactivate
