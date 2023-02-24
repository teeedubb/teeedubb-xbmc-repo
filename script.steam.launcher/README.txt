# Steam Launcher

Start Steam Big Picture Mode from within Kodi

See Kodi forum thread for more details:
http://forum.kodi.tv/showthread.php?tid=157499

https://github.com/teeedubb/teeedubb-xbmc-repo
http://store.steampowered.com/bigpicture
http://kodi.tv/

---

## Development

- Enable Debug Logging in Kodi to see if there are any issues with the add-on. (https://kodi.wiki/view/Log_file/Easy)

### Windows - Compiling the AHK script to an .exe file for use with the addon after modifications

1. Download v1 of AutoHotkey(https://www.autohotkey.com/download/)
2. Use a text editor such as Notepad++ or SciTE4AutoHotkey to make your changes to the steam-launcher.ahk script file(https://notepad-plus-plus.org/ or https://www.autohotkey.com/scite4ahk/)
3. Ensure you change the revision number in the ahk script to prevent your modified files from being overwritten during addon updates.
4. After you've made your changes, compile it into an `.exe` by opening Ahk2Exe.
      ```
      Source: <PATH_TO_SCRIPT>
      Destination: <KODI_USERDATA>\addon_data\script.steam.launcher\scripts\steam-launcher.exe
      Custom Icon: <PATH_TO_ICON>
      ```
   Click **Convert**
4. Move both the steam-launcher ahk and exe files to %AppData%\Kodi\userdata\addon_data\script.steam.launcher\scripts