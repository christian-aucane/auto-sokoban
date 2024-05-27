#!/bin/bash

python -m venv venv
if [ -d "venv/bin" ]; then
    VENV_PATH="venv/bin/activate"
# If not, check that the Scripts directory exists (for Windows)
elif [ -d "venv/Scripts" ]; then
    VENV_PATH="venv/Scripts/activate"
else
    echo "Error : Virtual environment directory not found."
    exit 1
fi

source $VENV_PATH
pip install -r requirements.txt

