@echo off
rem Stops their world. It saves first, and carries on from the same moment next time.
cd /d "%~dp0"
python -m acl stop
timeout /t 3 >nul
