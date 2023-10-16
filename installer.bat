@echo off
call :not_in_virtualenv
if %errorlevel% equ 0 (
    call python -m venv venv
    call venv\Scripts\activate
)

if not exist dist\assets mkdir dist\assets

xcopy /E /I assets\ dist\assets\
copy rotoview.ico dist\rotoview.ico
pip install -r requirements.txt
pip install pyinstaller
pyinstaller %*
call deactivate
exit /b 0

::Functions
::Functions
:not_in_virtualenv
:: Test if %VIRTUAL_ENV% is empty. Status code 0 when empty = return true
if "%VIRTUAL_ENV%"=="" ( exit /b 0) else (exit /b 1)