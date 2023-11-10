;Kodi Steam Launcher AutoHotKey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
;
;Manual script usage:
;steam-launcher.exe "e:\path\to\steam.exe" "d:\path\to\kodi.exe" "0/1" "true/false" "prescriptpath/false" "postscriptpath/false" "steam parameters" "0/seconds" "true/false" "false/string" "false/string"
;%1 Full path to Steam
;%2 Full path to Kodi
;%3 Quit or minimise Kodi - 0 to quit, 1 to minimise
;%4 Run Kodi in portable mode - true or false
;%5 Pre Steam script - false for none or full path to script
;%6 Post Steam script - false for none or full path to script
;%7 Additional command line parameters to pass to Steam (see https://developer.valvesoftware.com/wiki/Command_Line_Options)
;%8 Force kill Kodi and how long to wait for before terminating in seconds. 0 to disable
;%9 Run Steam desktop mode - true or false
;%10 Custom BPM window title - false or string
;%11 Custom DM window title - false or string
;
;Change the 'steam.launcher.script.revision =' number below to 999 to preserve changes through addon updates, otherwise it will be overwritten if the script is updated.
;You will need to have AutoHotKey installed to recompile this .ahk file into a .exe to work with the addon - see readme for more info.
;
;steam.launcher.script.revision=018

#NoEnv
#SingleInstance force
SetWorkingDir %A_ScriptDir%
;@Ahk2Exe-SetMainIcon steam-launcher.ico

if 0 != 11
{
	MsgBox This script requires 11 arguments but it only received %0%. See script file for details.
	ExitApp
}

IfEqual, 10, false
{
	GroupAdd, SteamBPM, Steam Big Picture Mode ahk_class SDL_app
}
Else
{
	GroupAdd, SteamBPM, %10%
}

IfEqual, 11, false
{
	GroupAdd, SteamDM, Steam ahk_class SDL_app
}
Else
{
	GroupAdd, SteamBPM, %11%
}

;pre steam script
IfNotEqual, 5, false
{
	RunWait, %5%,,Hide
}

;check if steam is running and launch or focus it
Process, Exist, Steam.exe
if ErrorLevel
{
	IfWinExist, ahk_group SteamBPM
	{
		WinActivate, ahk_group SteamBPM
		WinWait, ahk_group SteamBPM
;		Send {Esc}
	}
	IfEqual, 9, true
	{
		WinActivate, ahk_group SteamDM
		WinMaximize, ahk_group SteamDM
	}
	Else
	{
		Run, %1% %7% steam://open/bigpicture
	}
}
Else
{
	IfEqual, 9, true
	{
		Run, %1% %7%
	}
	Else
	{
		Run, %1% %7% -gamepadui
	}
}

SteamLoop:
;wait for steam
IfEqual, 9, true
{
	WinWait, ahk_group SteamDM
}
Else
{
	WinWait, ahk_group SteamBPM
}

;kill/minimise kodi
IfEqual, 3, 0
{
	Run, %comspec% /c taskkill /im kodi.exe,,Hide
	IfNotEqual, 8, 0
	{
		Run, %comspec% /c timeout /t %8% && tasklist /nh /fi "imagename eq kodi.exe" | find /i "kodi.exe" >nul && (taskkill /f /im kodi.exe),,Hide
	}
}
IfEqual, 3, 1
{
	WinMinimize, Kodi ahk_class Kodi
}

;steam detection loop
IfEqual, 9, true
{
	WinWait, ahk_group SteamDM
	WinActivate, ahk_group SteamDM
	loop
	{
		Process, Exist, Steam.exe
		if ErrorLevel
		{
			sleep, 500
		}
		Else
		{
			break
		}
	}
}
Else
{
	WinWait, ahk_group SteamBPM
	WinActivate, ahk_group SteamBPM
	loop
	{
		IfWinNotExist, ahk_group SteamBPM
		{
			BPMState = closed
			break
		}
		WinGet, MinMax, MinMax, ahk_group SteamBPM
		IfEqual MinMax, -1
		{
			break
			BPMState = minimised
		}
		Sleep, 500
	}
}

;post steam script
IfNotEqual, 6, false
{
	RunWait, %6%,,Hide
}

;launch/maximise kodi
IfEqual, 3, 0
{
	IfEqual, 4, true
	{
		Run, %2% -p
	}
	Else
	{
		Run, %2%
	}
}
IfEqual, 3, 1
{
	WinMaximize, Kodi ahk_class Kodi
}
;wait for kodi + activate
WinWait, Kodi ahk_class Kodi
WinActivate, Kodi ahk_class Kodi

;check if steam re-opened due to an update
IfEqual, 9, true
{
	WinWait, ahk_group SteamDM,,5
	if ErrorLevel
	{
		return
	}
	Else
	{
		IfNotEqual, 5, false
		{
			RunWait, %5%,,Hide
		}
		Goto, SteamLoop
	}
}
Else
{
	if BPMState = closed
	{
		WinWait, ahk_group SteamBPM,,5
		if ErrorLevel
		{
			return
		}
		Else
		{
			IfNotEqual, 5, false
			{
				RunWait, %5%,,Hide
			}
			Goto, SteamLoop
		}
	}
}
ExitApp