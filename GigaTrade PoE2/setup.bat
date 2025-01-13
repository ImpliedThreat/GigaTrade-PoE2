@echo off

set "venv_name=.venv"
if not exist %venv_name%\Scripts\activate (
    python -m venv %venv_name%
)
call "%venv_name%\Scripts\activate"
py -m pip install --upgrade pip
pip install -r requirements.txt
deactivate
pause
