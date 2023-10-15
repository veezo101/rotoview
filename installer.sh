#!/bin/bash
# Ensure the 'dist' and subdirectories exist
mkdir -p dist/assets

# Copy files and attempt to install dependencies
cp -R assets/ dist/
cp rotoview.ico dist/rotoview.ico
pip install -r requirements.txt
pip install pyinstaller

# Run PyInstaller with the provided arguments
pyinstaller "$@"