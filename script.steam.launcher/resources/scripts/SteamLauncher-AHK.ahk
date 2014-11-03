;KODI steam launcher autohotkey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
;Manual script usage: SteamLauncher-AHK.exe "e:\path\to\steam.exe" "d:\path\to\kodi.exe" "0/1" "true/false" "scriptpath/false" "scriptpath/false"
;$3 = 0 Quit KODI, 1 Minimize KODI. $4 = KODI portable mode. $5 = pre script. $6 post script.
;Change the 'steam.launcher.script.revision =' number below to 999 to preserve changes through addon updates, otherwise it shall be overwritten.
;You will need to have AutoHotKey installed to recompile this .ahk file into a .exe to work with the addon.
;
;steam.launcher.script.revision=007

#NoEnv  
#SingleInstance force
SetWorkingDir %A_ScriptDir%

if 0 != 6
{
    MsgBox This script requires arguments but it only received %0%. See script file for details.
    ExitApp
}

IfNotEqual, 5, false
{
	RunWait, %5%,,Hide
}

Process, Exist, Steam.exe
if ErrorLevel
{
    IfWinExist, Steam ahk_class CUIEngineWin32
	{
		WinActivate, Steam ahk_class CUIEngineWin32
	}
	else
	{
		Run, %1% steam://open/bigpicture
	}
}
else
{
    Run, %1% -bigpicture
}

GroupAdd, SteamBPM, Steam ahk_class CUIEngineWin32
GroupAdd, SteamBPM, Steam ahk_class Steam

SteamLoop:

WinWait, ahk_group SteamBPM
if %3%
{
	WinMinimize, Kodi ahk_class Kodi
}
else
{
	Run, %comspec% /c taskkill /im Kodi.exe,,Hide
	Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq Kodi.exe" | find /i "Kodi.exe" >nul && (taskkill /f /im Kodi.exe),,Hide
}
WinWait, Steam ahk_class CUIEngineWin32
WinActivate, Steam ahk_class CUIEngineWin32
WinWaitClose, Steam ahk_class CUIEngineWin32

IfNotEqual, 6, false
{
	RunWait, %6%,,Hide
}

if %3%
{
	WinMaximize, Kodi ahk_class Kodi
}
else
{
	IfEqual, 4, true
    {
        run, %2% -p
    }
    else
    {
	    run, %2%
	}
}
WinWait, Kodi ahk_class Kodi
WinActivate, Kodi ahk_class Kodi

WinWait, ahk_group SteamBPM,,5
if ErrorLevel
{
    return
}
else
{
    IfNotEqual, 5, false
    {
	    RunWait, %5%,,Hide
    }
    Goto, SteamLoop
}

ExitApp