;xbmc steam launcher autohotkey script by teeedubb
#NoEnv  
#SingleInstance force
SetWorkingDir %A_ScriptDir%

Process, Exist, Steam.exe
if ErrorLevel
{
    run, %1% steam://open/bigpicture &
}
else
{
    run, %1% -bigpicture &
}
sleep, 2000
Run %comspec% /c taskkill /f /im XBMC.exe,,Hide
sleep, 2000
WinActivate Steam ahk_class CUIEngineWin32
WinWait, Steam ahk_class CUIEngineWin32
WinWaitClose, Steam ahk_class CUIEngineWin32
	run, %2% &
ExitApp