;KODI steam launcher autohotkey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
;Manual script usage: SteamLauncher-AHK.exe "e:\path\to\steam.exe" "d:\path\to\kodi.exe" "0/1" "true/false" "scriptpath/false" "scriptpath/false" "steam parameters" "0" "true/false"
;$3 = 0 Quit KODI, 1 Minimize KODI. $4 = KODI portable mode. $5 = pre script. $6 post script. $7 steam parameters. $8 force kill kodi and how long to wait for. $9 launch steam in desktop mode.
;Change the 'steam.launcher.script.revision =' number below to 999 to preserve changes through addon updates, otherwise it shall be overwritten.
;You will need to have AutoHotKey installed to recompile this .ahk file into a .exe to work with the addon.
;
;steam.launcher.script.revision=013

#NoEnv  
#SingleInstance force
SetWorkingDir %A_ScriptDir%

if 0 != 9
{
    MsgBox This script requires 9 arguments but it only received %0%. See script file for details.
    ExitApp
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
    IfWinExist, Steam ahk_class CUIEngineWin32
	{
		WinActivate, Steam ahk_class CUIEngineWin32
		WinWait, Steam ahk_class CUIEngineWin32
		Send {Esc}
	}
	IfEqual, 9, true
	{
		WinActivate, Steam ahk_class vguiPopupWindow
		WinMaximize, Steam ahk_class vguiPopupWindow
	}
	else
	{
		Run, %1% %7% steam://open/bigpicture
	}
}
else
{
	IfEqual, 9, true
	{
		Run, %1% %7%
	}
	else
	{
		Run, %1% %7% -bigpicture
	}
}

GroupAdd, SteamBPM, Steam ahk_class CUIEngineWin32
GroupAdd, SteamBPM, Steam ahk_class steam

SteamLoop:
;wait for steam
IfEqual, 9, true
{
	WinWait, Steam ahk_class vguiPopupWindow
}
else
{
	WinWait, ahk_group SteamBPM
}

;kill/minimise kodi
IfEqual, 3, 0
{
	Run, %comspec% /c taskkill /im Kodi.exe,,Hide
	IfNotEqual, 8, 0
	{
		Run, %comspec% /c timeout /t %8% && tasklist /nh /fi "imagename eq Kodi.exe" | find /i "Kodi.exe" >nul && (taskkill /f /im Kodi.exe),,Hide
	}
}
IfEqual, 3, 1
{
	WinMinimize, Kodi ahk_class Kodi
}

;steam detection loop
IfEqual, 9, true
{
	WinWait, Steam ahk_class vguiPopupWindow
	WinActivate, Steam ahk_class vguiPopupWindow
	loop
	{
		Process, Exist, Steam.exe
		if ErrorLevel
		{
			sleep, 500
		}
		else
		{
			break
		}
	}
}
else
{
	WinWait, Steam ahk_class CUIEngineWin32
	WinActivate, Steam ahk_class CUIEngineWin32
	loop
	{
	  IfWinNotExist, Steam ahk_class CUIEngineWin32
	  {
		BPMState = closed
		break
	  }
	  WinGet, MinMax, MinMax, Steam ahk_class CUIEngineWin32
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
        run, %2% -p
    }
    else
    {
	    run, %2%
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
	WinWait, Steam ahk_class vguiPopupWindow,,5
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
}
else
{
	if BPMState = closed
	{
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
	}
}
ExitApp