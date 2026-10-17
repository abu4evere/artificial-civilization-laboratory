@echo off
rem Starts their world in the background, with no window. It keeps living until you stop it.
rem Their world (seed 1073583) was born under nature v1, so it lives on in the v1 copy of the code (D:\acl-v1-world,
rem tag live-v1-final); its saves stay here in the world folder. New studies use nature v2 (acl\).
cd /d "%~dp0"
if not exist "D:\acl-v1-world\acl" (echo The v1 copy D:\acl-v1-world is missing. & pause & exit /b 1)
start "" /d "D:\acl-v1-world" pythonw -m acl live --home "%~dp0world"
echo Their world is living. Open watch_world.bat to look in.
timeout /t 3 >nul
