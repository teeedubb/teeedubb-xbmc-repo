XBMC Steam Launcher.

A XBMC addon to launch Steam from within XBMC - It will close XBMC, launch Steam in Big Picture mode and when Steam is exited XBMC will restart. Steam also comes with a full featured web browser than can be controlled with a game pad or remote and plays back flash content. It works with Windows, Linux and quite possibly OSX, but this hasn't been tested.

Linux users need to make the script that launches Steam executable:

Code:
chmod +x ~/.xbmc/addons/script.steam.launcher/resources/scripts/steam-launch.sh

The settings within the addon should work provided Steam and XBMC are installed in their default directories. 
For non standard install locations etc you can edit the files used to launch:

Windows
Code:
%appdata%\XBMC\addons\script.steam.launcher\resources\scripts\steam-launch.bat

Windows version uses a AutoHotKey .exe to launch steam. AHK script is included in case you want to make changes to the default timeouts, eg: start steam, wait X seconds then kill xbmc. The ahk script will force focus on either xbmc/steam when they are run. Script usage is SteamLaunch-AHK.exe "d:\games\steam\steam.exe" "d:\xbmc\xbmc.exe"


Linux
Code:
~/.xbmc/addons/script.steam.launcher/resources/scripts/steam-launch.sh

http://forum.xbmc.org/showthread.php?tid=157499
http://store.steampowered.com/bigpicture
http://xbmc.org/