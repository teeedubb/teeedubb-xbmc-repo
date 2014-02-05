;xbmc steam launcher autohotkey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
#NoEnv  
#SingleInstance force
SetWorkingDir %A_ScriptDir%

Process, Exist, Steam.exe
if ErrorLevel
{
    if WinExist("ahk_class CUIEngineWin32")
	{
		WinActivate Steam ahk_class CUIEngineWin32
	}
	else
	{
		run, %1% steam://open/bigpicture
	}
}
else
{
    run, %1% -bigpicture
}

GroupAdd, SteamBPM, ahk_class CUIEngineWin32
GroupAdd, SteamBPM, ahk_class Steam

SteamLoop:

WinWait, ahk_group SteamBPM
if %3%
{
	WinMinimize, XBMC
}
else
{
	Run, %comspec% /c taskkill /f /im XBMC.exe,,Hide
}
WinWait, Steam ahk_class CUIEngineWin32
WinActivate, Steam ahk_class CUIEngineWin32
WinWaitClose, Steam ahk_class CUIEngineWin32

if %3%
{
	WinMaximize, XBMC
}
else
{
	run, %2%
}
WinWait, XBMC ahk_class XBMC
WinActivate, XBMC ahk_class XBMC

WinWait, ahk_group SteamBPM,,5
if ErrorLevel
{
    return
}
else
{
    Goto, SteamLoop
}

ExitApp