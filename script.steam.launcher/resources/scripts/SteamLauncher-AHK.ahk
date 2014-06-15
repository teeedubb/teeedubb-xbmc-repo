;xbmc steam launcher autohotkey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
;Manual script usage: SteamLauncher-AHK.exe "e:\path\to\steam.exe" "d:\path\to\xbmc.exe" "0/1"
;0 = Quit Steam. 1 = Minimize xbmc while steam is running.
;Edit this script to launch external programs before Steam or XBMC. See the three marked locations below.
;Change the 'steam.launcher.script.revision=' number below to 999 to preserve changes through addon updates, otherwise it shall be overwritten.
;You will need to have AutoHotKey installed to recompile this .ahk file into a .exe to work with the addon.
;
;steam.launcher.script.revision=003

#NoEnv  
#SingleInstance force
SetWorkingDir %A_ScriptDir%

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;Steam starts here, insert code below:
;eg: Run, %comspec% /c Z:\YOUR\COMMAND\HERE.EXE,,Hide
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

IfNotEqual, 5, false
{
	RunWait, %5%,,Hide
}

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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;XBMC restarts here, insert code below:
;eg: Run, %comspec% /c Z:\YOUR\COMMAND\HERE.EXE,,Hide
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

IfNotEqual, 6, false
{
	RunWait, %6%,,Hide
}

if %3%
{
	WinMaximize, XBMC
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
WinWait, XBMC ahk_class XBMC
WinActivate, XBMC ahk_class XBMC

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
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;Steam can restart here due to Steam client updates, insert code below:
    ;eg: Run, %comspec% /c Z:\YOUR\COMMAND\HERE.EXE,,Hide
	;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

}

ExitApp