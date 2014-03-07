@echo helllllllllllllllo
@echo off
echo XBMC Steam BPM launcher by teeedubb.
echo Check for 64bit or 32bit Windows:
IF EXIST "%PROGRAMFILES(X86)%" (
echo Running 64-bit Windows.
set PRGMFiles="C:\Program Files (x86)"
) || (
echo Running 32-bit Windows.
set PRGMFiles="C:\Program Files"
)

REM ##############################################################
REM OPTIONS
REM Configure the following 3 entries:
REM EG:
REM set STEAMLaunchCmd="D:\games\steam\steam.exe"

set XBMCLaunchCmd=%PRGMFiles%\XBMC\XBMC.exe
set STEAMLaunchCmd=%PRGMFiles%\Steam\steam.exe

set STEAMLauncherCmd="%appdata%/XBMC/addons/script.steam.launcher/resources/scripts/SteamLauncher-AHK.exe"
REM ##############################################################


%STEAMLauncherCmd% %STEAMLaunchCmd% %XBMCLaunchCmd%