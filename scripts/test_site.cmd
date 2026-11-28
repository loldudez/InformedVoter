@echo off
rem The test site: this folder as it is right now, at http://localhost:8770, on this
rem computer only. Every change made in this folder shows there on a reload, while
rem www.informedvoter.io changes only when the GitHub folder is pushed from GitHub
rem Desktop. Double-click this file to start it: the site runs in a window of its own,
rem titled "Informed Voter test site"; close that window to stop it.
cd /d "%~dp0.."
set "PY=%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe"
if not exist "%PY%" set "PY=%LOCALAPPDATA%\Python\bin\python.exe"
start "Informed Voter test site" "%PY%" scripts\serve.py 8770
timeout /t 2 /nobreak >nul
start "" http://localhost:8770/
