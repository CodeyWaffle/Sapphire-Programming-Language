//Sapphire Programming Language Installer v1.1
@echo off
setlocal enabledelayedexpansion
title Sapphire Studio Launcher
chcp 65001 >nul
cls

:: --- PATH SETTINGS ---
set "BASE_DIR=%~dp0"
set "CONFIG_DIR=%BASE_DIR%config"
set "WORKSPACE=%BASE_DIR%SapphireProjects"
set "ICON_256=%CONFIG_DIR%\icon_256.ico"

:: 1. CREATE FOLDERS
echo [SYSTEM] Setting up directories...
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"
if not exist "%WORKSPACE%" mkdir "%WORKSPACE%"

:: 2. SYNC FILES (Move any strays into config)
echo [SYSTEM] Syncing files...
if exist "%BASE_DIR%Sapphire*.py" move /y "%BASE_DIR%Sapphire*.py" "%CONFIG_DIR%\" >nul
if exist "%BASE_DIR%*.ico" move /y "%BASE_DIR%*.ico" "%CONFIG_DIR%\" >nul

:: 3. CREATE DESKTOP SHORTCUT
echo [SYSTEM] Creating desktop shortcut...
if not exist "%USERPROFILE%\Desktop\Sapphire Studio v1.1.lnk" (
    powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\Sapphire Studio v1.1.lnk');$s.TargetPath='%~f0';$s.IconLocation='%ICON_256%';$s.Save()"
)

:: 4. LAUNCH
echo [SYSTEM] Launching Sapphire Studio...
cd /d "%CONFIG_DIR%"
echo [SYSTEM] Keep this terminal open to run Sapphire Studio. Close it to exit.
python SapphireStudio11.py