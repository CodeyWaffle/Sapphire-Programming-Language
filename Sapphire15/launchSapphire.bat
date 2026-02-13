@echo off
setlocal enabledelayedexpansion
title Sapphire Studio Workspace Loader
cls

echo 💎 Sapphire Workspace Initializing...

:: 1. Create Workspace
if not exist "Sapphire_Project" mkdir "Sapphire_Project"

:: 2. Find the NEWEST Sapphire library (highest number)
set "NEWEST_LIB="
for /f "delims=" %%i in ('dir /b /o-n Sapphire*.py') do (
    if "%%i" neq "SapphireStudio.py" (
        if not defined NEWEST_LIB set "NEWEST_LIB=%%i"
    )
)

if defined NEWEST_LIB (
    echo [SYSTEM] Found Newest Library: !NEWEST_LIB!
    copy "!NEWEST_LIB!" "Sapphire_Project\" >nul
)

:: 3. Clean up and Move Files
if exist *.sp move *.sp "Sapphire_Project\" >nul
if exist SapphireStudio.py copy SapphireStudio.py "Sapphire_Project\" >nul

:: 4. Launch
cd "Sapphire_Project"
echo [SUCCESS] Workspace Ready.
python SapphireStudio.py
pause