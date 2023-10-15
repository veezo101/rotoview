@echo off

if not exist dist\assets mkdir dist\assets

xcopy /E /I assets\ dist\assets\
copy rotoview.ico dist\rotoview.ico
pip install -r requirements.txt
pip install pyinstaller
pyinstaller %*