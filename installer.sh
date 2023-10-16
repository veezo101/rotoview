#!/bin/bash

not_in_virtualenv() {
    #test if $VIRTUAL_ENV is empty. status code 0 when empty = return true
    [[ -z "$VIRTUAL_ENV" ]]
}

# Ensure we are in Virtual Env
if not_in_virtualenv; then
    python -m venv venv
    source ./venv/Scripts/activate
fi

# Ensure the 'dist' and subdirectories exist
mkdir -p dist/assets

# Copy files and attempt to install dependencies
cp -R assets/ dist/
cp rotoview.ico dist/rotoview.ico
pip install -r requirements.txt
pip install pyinstaller

# Run PyInstaller with the provided arguments
pyinstaller "$@"