@echo off
title Anil Dutta - World News Map Platform
echo ==============================================================
echo        Starting World News Map Platform...
echo ==============================================================
echo.
cd /d "%~dp0"

set "PATH=%LOCALAPPDATA%\Python\bin;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python313;%LOCALAPPDATA%\Programs\Python\Python314;%PATH%"

py server.py

if errorlevel 1 (
    python server.py
)

if errorlevel 1 (
    echo Launching index.html directly...
    start "" index.html
)
pause
