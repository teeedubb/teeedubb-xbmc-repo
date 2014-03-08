Steam Launcher - Start Steam Big Picture Mode from within XBMC

This add-on will close XBMC, launch Steam in Big Picture mode and when Steam is exited XBMC will restart. It works with Windows and Linux (quite possibly OSX, but this hasnt been tested). XBMCbuntu users read here first. A nice bonus is Steam also comes with a full featured web browser that can be controlled with a game pad or remote and plays back flash content.

Settings:
General:
-Select whether to quit XBMC: Options are Yes, No and Ask. 
-Here you can change the paths for both XBMC and Steam.

Advanced:
-Delete scripts and update on next run - delete the OS specific scripts out of the profile://addon_data directory and copy them from the addon install directory the next time the addon is run. This is handy if you want to go back to the default scripts or if the bundled scripts have been updated. Only the script file will be deleted and the setting is turned off (to default) when run once.
-Configurable timeout for 'Busy Dialog" after running addon.
-Script update notification.
-Linux only: Make steam-launch.sh executable on next run - This changes the executable bit on the file 'steam-launch.sh' which is necessary for this addon to run, Linux users need to do this on the first run and after deleting the profile://addon_data scripts. This setting defaults to off after being run once. Linux users also need the program 'wmctrl' installed - theres a good chance it already is on a desktop install.
-Windows only: Use a Batch file to launch scripts - Use a batch file as in previous version which should hopefully solve the 'nothing happening' issue some people have been having. GUI settings for XBMC + Steam paths and whether to quit XBMC have no effect with this setting enabled, the options are configured via steam-launch.bat, located in userdata/addon_data/script.steam.launcher/scripts/ , with instructions located in file itself. steam-launch.bat is not deleted by the addon or updates and if it does not exist it will be copied to the userdata directory on first run with the option enabled, along with launchhidden-bat.vbs


Customisation:
The scripts used by this addon can be customised to suit your needs, they reside in profile://addon_data/scripts folder. They are copied into that directory from the addon install directory on first run and they will not be over written with updates, only via the advanced addon settings.

https://github.com/teeedubb
http://forum.xbmc.org/showthread.php?tid=157499
http://store.steampowered.com/bigpicture
http://xbmc.org/