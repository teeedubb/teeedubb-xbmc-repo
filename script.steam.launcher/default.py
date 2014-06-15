# steam launcher by teeedubb. http://forum.xbmc.org/showthread.php?tid=157499
# I used Rom Collection Browser as a guide when making this addon, plus borrowed ideas and code from it too. Big thanks to malte for RCB!
import os
import sys
import subprocess
import time
import shutil
import stat

import xbmcaddon
import xbmc
import xbmcgui


addon = xbmcaddon.Addon(id='script.steam.launcher')
addonPath = addon.getAddonInfo('path')
addonIcon = addon.getAddonInfo('icon')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
scriptid = 'script.steam.launcher'

steamLinux = addon.getSetting("SteamLinux")
xbmcLinux = addon.getSetting("XbmcLinux")
steamWin = addon.getSetting("SteamWin")
xbmcWin = addon.getSetting("XbmcWin")
steamOsx = addon.getSetting("SteamOsx")
xbmcOsx = addon.getSetting("XbmcOsx")
delUserScriptSett = addon.getSetting("DelUserScript")
makeShExec = addon.getSetting("MakeShExec")
quitXbmcSetting = addon.getSetting("QuitXbmc")
busyDialogTime = int(addon.getSetting("BusyDialogTime"))
scriptUpdateCheck = addon.getSetting("ScriptUpdateCheck")
filePathCheck = addon.getSetting("FilePathCheck")
xbmcPortable = addon.getSetting("XbmcPortable")
preScriptEnabled = addon.getSetting("PreScriptEnabled")
preScript = addon.getSetting("PreScript")
postScriptEnabled = addon.getSetting("PostScriptEnabled")
postScript = addon.getSetting("PostScript")


def log(msg):
    xbmc.log(u'%s: %s' % (scriptid, msg))


def getAddonInstallPath():
    path = addon.getAddonInfo('path')
    return path


def getAddonDataPath():
    path = xbmc.translatePath('special://profile/addon_data/%s' % (scriptid))
    if not os.path.exists(path):
        log('addon userdata folder does not exist, creating: %s' % path)
        try:
            os.makedirs(path)
        except:
            path = ''
            log('failed to create: %s' % path)
    return path


def copyLauncherScriptsToUserdata():
    oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
    newBasePath = os.path.join(getAddonDataPath(), 'scripts')
    if os.name == 'nt':
        oldPath = os.path.join(oldBasePath, 'LaunchHidden.vbs')
        newPath = os.path.join(newBasePath, 'LaunchHidden.vbs')
        copyFile(oldPath, newPath)

        oldPath = os.path.join(oldBasePath, 'SteamLauncher-AHK.ahk')
        newPath = os.path.join(newBasePath, 'SteamLauncher-AHK.ahk')
        copyFile(oldPath, newPath)

        oldPath = os.path.join(oldBasePath, 'SteamLauncher-AHK.exe')
        newPath = os.path.join(newBasePath, 'SteamLauncher-AHK.exe')
        copyFile(oldPath, newPath)

    else:
        oldPath = os.path.join(oldBasePath, 'steam-launch.sh')
        newPath = os.path.join(newBasePath, 'steam-launch.sh')
        copyFile(oldPath, newPath)


def copyFile(oldPath, newPath):
    newDir = os.path.dirname(newPath)
    if not os.path.isdir(newDir):
        log('userdata scripts folder does not exist, creating: %s' % newDir)
        try:
            os.mkdir(newDir)
        except:
            log('failed to create: %s' % newDir)
            return

    if not os.path.isfile(newPath):
        log('file does not exist, copying to userdata: %s' % newPath)
        try:
            shutil.copy2(oldPath, newPath)
        except:
            log('failed to create: %s' % newPath)
            return


def programFileCheck():
    if os.name == 'nt':
        global steamWin
        global xbmcWin
        steamWin = addon.getSetting("SteamWin")
        if not os.path.isfile(os.path.join(steamWin)):
            log('file does not exist: %s' % steamWin)
            if dialog.yesno("" + language(50123) + "", "" + steamWin + "", "" + language(50120) + "",
                            "" + language(50121) + ""):
                log('opening addon settings')
                addon.openSettings()
                steamWin = addon.getSetting("SteamWin")
                if not os.path.isfile(os.path.join(steamWin)):
                    log('still not found, exiting: %s' % steamWin)
                    sys.exit()
            else:
                log('exiting')
                sys.exit()
        xbmcWin = addon.getSetting("XbmcWin")
        if not os.path.isfile(os.path.join(xbmcWin)):
            log('file does not exist: %s' % xbmcWin)
            if dialog.yesno("" + language(50123) + "", "" + xbmcWin + "", "" + language(50120) + "",
                            "" + language(50121) + ""):
                log('opening addon settings')
                addon.openSettings()
                xbmcWin = addon.getSetting("XbmcWin")
                if not os.path.isfile(os.path.join(xbmcWin)):
                    log('still not found, exiting: %s' % xbmcWin)
                    sys.exit()
            else:
                log('exiting')
                sys.exit()
    else:
        if sys.platform == "darwin":
            global steamOsx
            global xbmcOsx
            steamOsx = addon.getSetting("SteamOsx")
            if not os.path.isdir(os.path.join(steamOsx)):
                log('folder does not exist: %s' % steamOsx)
                if dialog.yesno("" + language(50123) + "", "" + steamOsx + "", "" + language(50120) + "",
                                "" + language(50121) + ""):
                    log('opening addon settings')
                    addon.openSettings()
                    steamOsx = addon.getSetting("SteamOsx")
                    if not os.path.isfile(os.path.join(steamOsx)):
                        log('still not found, exiting: %s' % steamOsx)
                        sys.exit()
                else:
                    log('exiting')
                    sys.exit()
            xbmcOsx = addon.getSetting("XbmcOsx")
            if not os.path.isdir(os.path.join(xbmcOsx)):
                log('folder does not exist: %s' % xbmcOsx)
                if dialog.yesno("" + language(50123) + "", "" + xbmcOsx + "", "" + language(50120) + "",
                                "" + language(50121) + ""):
                    log('opening addon settings')
                    addon.openSettings()
                    xbmcOsx = addon.getSetting("XbmcOsx")
                if not os.path.isfile(os.path.join(xbmcOsx)):
                    log('still not found, exiting: %s' % xbmcOsx)
                    sys.exit()
                else:
                    log('exiting')
                    sys.exit()
        else:
            global steamLinux
            global xbmcLinux
            if not os.path.isfile(os.path.join(steamLinux)):
                log('file does not exist: %s' % steamLinux)
                steamLinux = addon.getSetting("SteamLinux")
                if dialog.yesno("" + language(50123) + "", "" + steamLinux + "", "" + language(50120) + "",
                                "" + language(50121) + ""):
                    log('opening addon settings')
                    addon.openSettings()
                    steamLinux = addon.getSetting("SteamLinux")
                    if not os.path.isfile(os.path.join(steamLinux)):
                        log('still not found, exiting: %s' % steamLinux)
                        sys.exit()
                else:
                    log('exiting')
                    sys.exit()
            if not os.path.isfile(os.path.join(xbmcLinux)):
                log('file does not exist: %s' % xbmcLinux)
                xbmcLinux = addon.getSetting("XbmcLinux")
                if dialog.yesno("" + language(50123) + "", "" + xbmcLinux + "", "" + language(50122) + "",
                                "" + language(50121) + ""):
                    log('opening addon settings')
                    addon.openSettings()
                    xbmcLinux = addon.getSetting("XbmcLinux")
                    if not os.path.isfile(os.path.join(xbmcLinux)):
                        log('still not found, exiting: %s' % xbmcLinux)
                        sys.exit()
                else:
                    log('exiting')
                    sys.exit()


def MakeShExecCheck():
    global makeShExec
    basePath = os.path.join(getAddonDataPath(), 'scripts')
    if not os.name == 'nt':
        if not stat.S_IXUSR & os.stat(os.path.join(basePath, 'steam-launch.sh'))[stat.ST_MODE]:
            log('steam-launch.sh is not executable')
            if makeShExec == 'false':
                if dialog.yesno("" + language(50123) + "", "" + os.path.join(basePath, 'steam-launch.sh') + "",
                                "" + language(50122) + "", "" + language(50121) + ""):
                    log('opening addon settings')
                    addon.openSettings()
                else:
                    log('exiting')
                    sys.exit()
            else:
                log('steam-launch.sh is not executable but is set be be made so')


def delUserScript():
    log('deleting user_data scripts')
    basePath = os.path.join(getAddonDataPath(), 'scripts')
    if os.path.isfile(os.path.join(basePath, 'SteamLauncher-AHK.ahk')):
        filePath = os.path.join(basePath, 'SteamLauncher-AHK.ahk')
        try:
            os.remove(filePath)
            log('found and deleting: %s' % filePath)
        except:
            log('deleting failed: %s' % filePath)
    if os.path.isfile(os.path.join(basePath, 'SteamLauncher-AHK.exe')):
        filePath = os.path.join(basePath, 'SteamLauncher-AHK.exe')
        try:
            os.remove(filePath)
            log('found and deleting: %s' % filePath)
        except:
            log('deleting failed: %s' % filePath)
    if os.path.isfile(os.path.join(basePath, 'LaunchHidden.vbs')):
        filePath = os.path.join(basePath, 'LaunchHidden.vbs')
        try:
            os.remove(filePath)
            log('found and deleting: %s' % filePath)
        except:
            log('deleting failed: %s' % filePath)
    if os.path.isfile(os.path.join(basePath, 'steam-launch.sh')):
        filePath = os.path.join(basePath, 'steam-launch.sh')
        try:
            os.remove(filePath)
            log('found and deleting: %s' % filePath)
        except:
            log('deleting failed: %s' % filePath)
    addon.setSetting(id="DelUserScript", value="false")


def scriptVersionCheck():
    global delUserScriptSett
    oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
    newBasePath = os.path.join(getAddonDataPath(), 'scripts')
    if delUserScriptSett == 'false':
        if os.name == 'nt':
            if os.path.isfile(os.path.join(newBasePath, 'SteamLauncher-AHK.ahk')):
                for line in open(os.path.join(oldBasePath, 'SteamLauncher-AHK.ahk'), "r"):
                    if "steam.launcher.script.revision=" in line:
                        scriptAhkSys = line[32:]
                for line in open(os.path.join(newBasePath, 'SteamLauncher-AHK.ahk'), "r"):
                    if not "steam.launcher.script.revision=" in line:
                        scriptAhkUsr = '000'
                for line in open(os.path.join(newBasePath, 'SteamLauncher-AHK.ahk'), "r"):
                    if "steam.launcher.script.revision=" in line:
                        scriptAhkUsr = line[32:]
                if scriptAhkSys > scriptAhkUsr:
                    log('addon scripts have been updated: %s' % scriptAhkSys > scriptAhkUsr)
                    if dialog.yesno("Steam Launcher", "" + language(50124) + "", "" + language(50121) + "",
                                    "" + language(50125) + ""):
                        addon.openSettings()
                        delUserScriptSett = addon.getSetting("DelUserScript")
                        if delUserScriptSett == 'true':
                            log('deleting old userdata scripts')
                            delUserScript()
                    else:
                        log('no selected, script update check disabled')
                        addon.setSetting(id="ScriptUpdateCheck", value="1")

        else:
            if os.path.isfile(os.path.join(newBasePath, 'steam-launch.sh')):
                for line in open(os.path.join(oldBasePath, 'steam-launch.sh'), "r"):
                    if "steam.launcher.script.revision=" in line:
                        scriptAhkSys = line[32:]
                for line in open(os.path.join(newBasePath, 'steam-launch.sh'), "r"):
                    if not "steam.launcher.script.revision=" in line:
                        scriptAhkUsr = '000'
                for line in open(os.path.join(newBasePath, 'steam-launch.sh'), "r"):
                    if "steam.launcher.script.revision=" in line:
                        scriptAhkUsr = line[32:]
                if scriptAhkSys > scriptAhkUsr:
                    log('addon scripts have been updated: %s' % scriptAhkSys > scriptAhkUsr)
                    if dialog.yesno("Steam Launcher", "" + language(50124) + "", "" + language(50121) + "",
                                    "" + language(50125) + ""):
                        addon.openSettings()
                        delUserScriptSett = addon.getSetting("DelUserScript")
                        if delUserScriptSett == 'true':
                            log('deleting old userdata scripts')
                            delUserScript()
                    else:
                        log('no selected, script update check disabled')
                        addon.setSetting(id="ScriptUpdateCheck", value="1")
    else:
        log('scripts are set to be deleted, no update check needed')


def quitXbmcDialog():
    global quitXbmcSetting
    if quitXbmcSetting == '2':
        if dialog.yesno("Steam Launcher", "" + language(50073) + ""):
            quitXbmcSetting = '0'
        else:
            quitXbmcSetting = '1'


def launchSteam():
    global postScript
    global preScript
    basePath = os.path.join(getAddonDataPath(), 'scripts')
    if preScriptEnabled == 'false':
        preScript = 'false'
    if postScriptEnabled == 'false':
        postScript = 'false'
    if preScript == '':
        preScript = 'false'
    if postScript == '':
        postScript = 'false'
    if os.name == 'nt':
        launchhidden = os.path.join(basePath, 'LaunchHidden.vbs')
        steamlauncher = os.path.join(basePath, 'SteamLauncher-AHK.exe')
        cmd = "\"" + launchhidden + "\"" + " " + "\"" + steamlauncher + "\"" + " " + "\"" + steamWin + "\"" + " " + "\"" + xbmcWin + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
        # cmd = "call" + " " + "\"" + launchhidden + "\"" + " " + "\"" + steamlauncher + "\"" + " " + "\"" + steamWin + "\"" + " " + "\"" + xbmcWin + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
        if makeShExec == 'true':
            addon.setSetting(id="MakeShExec", value="false")
            log('steam-launch.sh doesnt exist in windows, option disabled')
        try:
            log('attempting to launch: %s' % cmd)
            subprocess.Popen(cmd, shell=True)
            # os.system(cmd)
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            time.sleep(busyDialogTime)
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        except:
            log('failed to run: %s' % cmd)
            xbmc.executebuiltin("Notification(" + language(50123) + "," + language(50126) + ",10000," + addonIcon + ")")
    else:
        steamlauncher = os.path.join(basePath, 'steam-launch.sh')
        if makeShExec == 'true':
            os.chmod(steamlauncher, stat.S_IRWXU)
            addon.setSetting(id="MakeShExec", value="false")
            log('steam-launch.sh should now be executable and the option disabled')
        if not stat.S_IXUSR & os.stat(os.path.join(basePath, 'steam-launch.sh'))[stat.ST_MODE]:
            log('steam-launch.sh is not executable, exiting')
            sys.exit()
        if sys.platform == "darwin":
            cmd = "\"" + steamlauncher + "\"" + " " + "\"" + steamOsx + "\"" + " " + "\"" + xbmcOsx + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
            try:
                log('attempting to launch: %s' % cmd)
                subprocess.Popen(cmd, shell=True)
                xbmc.executebuiltin("ActivateWindow(busydialog)")
                time.sleep(busyDialogTime)
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            except:
                log('failed to launch: %s' % cmd)
                xbmc.executebuiltin(
                    "Notification(" + language(50123) + "," + language(50126) + ",10000," + addonIcon + ")")
        else:
            cmd = "\"" + steamlauncher + "\"" + " " + "\"" + steamLinux + "\"" + " " + "\"" + xbmcLinux + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
            try:
                log('attempting to launch: %s' % cmd)
                subprocess.Popen(cmd, shell=True)
                xbmc.executebuiltin("ActivateWindow(busydialog)")
                time.sleep(busyDialogTime)
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            except:
                log('failed to launch: %s' % cmd)
                xbmc.executebuiltin(
                    "Notification(" + language(50123) + "," + language(50126) + ",10000," + addonIcon + ")")


if scriptUpdateCheck == '0':
    scriptVersionCheck()
    log('running script version check')
else:
    log('script version check disabled')

if delUserScriptSett == 'true':
    log('delete userdata script option enabled')
    delUserScript()

copyLauncherScriptsToUserdata()
log('checking for and copying userdata scripts')

if not os.name == 'nt':
    if makeShExec == 'false':
        MakeShExecCheck()
        log('checking if steam-launch.sh is executable')

if filePathCheck == '0':
    log('running program file check')
    programFileCheck()
else:
    log('program file check disabled')

quitXbmcDialog()

log('running steam...')
if os.name == 'nt':
    log('steamWin: %s' % steamWin)
    log('xbmcWin: %s' % xbmcWin)
else:
    if sys.platform == "darwin":
        log('steamOsx: %s' % steamOsx)
        log('xbmcOsx: %s' % xbmcOsx)
    else:
        log('steamLinux: %s' % steamLinux)
        log('xbmcLinux: %s' % xbmcLinux)
log('delUserScriptSett: %s' % delUserScriptSett)
log('makeShExec: %s' % makeShExec)
log('quitXbmcSetting: %s' % quitXbmcSetting)
log('busyDialogTime: %s' % busyDialogTime)
log('scriptUpdateCheck: %s' % scriptUpdateCheck)
log('filePathCheck: %s' % filePathCheck)
log('xbmcPortable: %s' % xbmcPortable)
log('preScriptEnabled: %s' % preScriptEnabled)
log('preScript: %s' % preScript)
log('postScriptEnabled: %s' % postScriptEnabled)
log('postScript: %s' % postScript)
launchSteam()