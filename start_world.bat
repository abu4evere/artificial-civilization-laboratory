@echo off
rem Starts their world in the background, with no window. It keeps living until you stop it.
cd /d "%~dp0"
start "" pythonw -m acl live
echo Their world is living. Open watch_world.bat to look in.
timeout /t 3 >nul
