# steam launcher by teeedubb. http://forum.xbmc.org/showthread.php?tid=157499
# I used Rom Collection Browser as a guide when making this addon, plus borrowed ideas and code from it too. Big thanks to malte for RCB!
import os
import sys
import subprocess
import time
import shutil
import stat

import xbmc

import xbmcaddon
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
scriptErrorNotification = "dialog.notification(language(50123), language(50126), addonIcon, 5000)"


osWin = xbmc.getCondVisibility('system.platform.windows')
osOsx = xbmc.getCondVisibility('system.platform.osx')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osAndroid = xbmc.getCondVisibility('system.platform.android')

def log(msg):
    xbmc.log(u'%s: %s' % (scriptid, msg))


def getAddonInstallPath():
    path = addon.getAddonInfo('path')
    return path


def getAddonDataPath():
    path = xbmc.translatePath('special://profile/addon_data/%s' % scriptid)
    if not os.path.exists(path):
        log('addon userdata folder does not exist, creating: %s' % path)
        try:
            os.makedirs(path)
            log('created directory: %s' % path)
        except:
            log('ERROR: failed to create directory: %s' % path)
            scriptErrorNotification
    return path


def copyLauncherScriptsToUserdata():
    oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
    newBasePath = os.path.join(getAddonDataPath(), 'scripts')
    if osWin:
        oldPath = os.path.join(oldBasePath, 'LaunchHidden.vbs')
        newPath = os.path.join(newBasePath, 'LaunchHidden.vbs')
        copyFile(oldPath, newPath)
        oldPath = os.path.join(oldBasePath, 'SteamLauncher-AHK.ahk')
        newPath = os.path.join(newBasePath, 'SteamLauncher-AHK.ahk')
        copyFile(oldPath, newPath)
        oldPath = os.path.join(oldBasePath, 'SteamLauncher-AHK.exe')
        newPath = os.path.join(newBasePath, 'SteamLauncher-AHK.exe')
        copyFile(oldPath, newPath)
    elif osLinux + osOsx:
        oldPath = os.path.join(oldBasePath, 'steam-launch.sh')
        newPath = os.path.join(newBasePath, 'steam-launch.sh')
        copyFile(oldPath, newPath)


def copyFile(oldPath, newPath):
    newDir = os.path.dirname(newPath)
    if not os.path.isdir(newDir):
        log('userdata scripts folder does not exist, creating: %s' % newDir)
        try:
            os.mkdir(newDir)
            log('sucsessfully created userdata scripts folder: %s' % newDir)
        except:
            log('ERROR: failed to create userdata scripts folder: %s' % newDir)
            scriptErrorNotification
            sys.exit()
    if not os.path.isfile(newPath):
        log('script file does not exist, copying to userdata: %s' % newPath)
        try:
            shutil.copy2(oldPath, newPath)
            log('sucsessfully copied userdata script: %s' % newPath)
        except:
            log('ERROR: failed to copy script file to userdata: %s' % newPath)
            scriptErrorNotification
            sys.exit()
    else:
        log('script file already exists, skipping copy to userdata: %s' % newPath)


def makeScriptExec():
    scriptPath = os.path.join(getAddonDataPath(), 'scripts', 'steam-launch.sh')
    if os.path.isfile(scriptPath):
        if not stat.S_IXUSR & os.stat(scriptPath)[stat.ST_MODE]:
            log('steam-launch.sh not executable: %s' % scriptPath)
            try:
                os.chmod(scriptPath, stat.S_IRWXU)
                log('steam-launch.sh now executable: %s' % scriptPath)
            except:
                log('ERROR: unable to make steam-launch.sh executable, exiting: %s' % scriptPath)
                scriptErrorNotification
                sys.exit()
            log('steam-launch.sh executable: %s' % scriptPath)


def usrScriptDelete():
    if delUserScriptSett == 'true':
        log('deleting userdata scripts, option enabled: delUserScriptSett = %s' % delUserScriptSett)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'SteamLauncher-AHK.ahk')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'SteamLauncher-AHK.exe')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'LaunchHidden.vbs')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'steam-launch.sh')
        delUserScript(scriptFile)
    elif delUserScriptSett == 'false':
        log('skipping deleting userdata scripts, option disabled: delUserScriptSett = %s' % delUserScriptSett)


def delUserScript(scriptFile):
    if os.path.isfile(scriptFile):
        try:
            os.remove(scriptFile)
            log('found and deleting: %s' % scriptFile)
        except:
            log('ERROR: deleting failed: %s' % scriptFile)
            scriptErrorNotification
        addon.setSetting(id="DelUserScript", value="false")


def fileChecker():
    if filePathCheck == 'true':
        log('running program file check, option is enabled: filePathCheck = %s' % filePathCheck)
        if osWin:
            steamWin = addon.getSetting("SteamWin")
            xbmcWin = addon.getSetting("XbmcWin")
            steamExe = os.path.join(steamWin)
            xbmcExe = os.path.join(xbmcWin)
            programFileCheck(steamExe, xbmcExe)
        elif osOsx:
            steamOsx = addon.getSetting("SteamOsx")
            xbmcOsx = addon.getSetting("XbmcOsx")
            steamExe = os.path.join(steamOsx)
            xbmcExe = os.path.join(xbmcOsx)
            programFileCheck(steamExe, xbmcExe)
        elif osLinux:
            steamLinux = addon.getSetting("SteamLinux")
            xbmcLinux = addon.getSetting("XbmcLinux")
            steamExe = os.path.join(steamLinux)
            xbmcExe = os.path.join(xbmcLinux)
            programFileCheck(steamExe, xbmcExe)
    else:
        log('skipping program file check, option disabled: filePathCheck = %s' % filePathCheck)


def fileCheckDialog(programExe):
    log('ERROR: dialog to go to addon settings because executable does not exist: %s' % programExe)
    if dialog.yesno(""+ language(50123) +"", ""+ programExe +"", ""+ language(50120) +"", ""+ language(50121) +""):
        log('yes selected, opening addon settings')
        addon.openSettings()
        fileChecker()
    else:
        log('ERROR: no selected with invalid executable, exiting: %s' % programExe)
        sys.exit()


def programFileCheck(steamExe, xbmcExe):
    if osWin + osLinux:
        if not os.path.isfile(os.path.join(steamExe)):
            fileCheckDialog(programExe)
        if not os.path.isfile(os.path.join(xbmcExe)):
            fileCheckDialog(programExe)
    if osOsx:
        if not os.path.isdir(os.path.join(steamExe)):
            fileCheckDialog(programExe)
        if not os.path.isdir(os.path.join(xbmcExe)):
            fileCheckDialog(programExe)


def scriptVersionCheck():
    if scriptUpdateCheck == 'true':
        log('usr scripts are set to be checked for updates...')
        if delUserScriptSett == 'false':
            log('usr scripts are not set to be deleted, running version check')
            sysScriptDir = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
            usrScriptDir = os.path.join(getAddonDataPath(), 'scripts')
            if osWin:
                sysScriptPath = os.path.join(sysScriptDir, 'SteamLauncher-AHK.ahk')
                usrScriptPath = os.path.join(usrScriptDir, 'SteamLauncher-AHK.ahk')
                if os.path.isfile(os.path.join(usrScriptPath)):
                    compareFile(sysScriptPath, usrScriptPath)
                else:
                    log('usr script does not exist, skipping version check')
            elif osLinux + osOsx:
                sysScriptPath = os.path.join(sysScriptDir, 'steam-launch.sh')
                usrScriptPath = os.path.join(usrScriptDir, 'steam-launch.sh')
                if os.path.isfile(os.path.join(usrScriptPath)):
                    compareFile(sysScriptPath, usrScriptPath)
                else:
                    log('usr script does not exist, skipping version check')
        else:
            log('usr scripts are set to be deleted, no version check needed')
    else:
        log('usr scripts are set to not be checked for updates, skipping version check')


def compareFile(sysScriptPath, usrScriptPath):
    global delUserScriptSett
    if os.path.isfile(sysScriptPath):
        with open(sysScriptPath) as f:
            for line in f.readlines():
                if "steam.launcher.script.revision=" in line:
                    scriptSysVer = line[32:]
                    if scriptSysVer == '':
                        scriptSysVer = '000'
                        log('"steam.launcher.script.revision=" number not found in script: %s' % sysScriptPath)
                    log('sys "steam.launcher.script.revision=": %s' % scriptSysVer)
    if os.path.isfile(usrScriptPath):
        with open(usrScriptPath, 'r') as f:
            for line in f.readlines():
                if "steam.launcher.script.revision=" in line:
                    scriptUsrVer = line[32:]
                    if scriptUsrVer == '':
                        scriptUsrVer = '000'
                        log('"steam.launcher.script.revision=" number not found in script: %s' % usrScriptPath)
                    log('usr "steam.launcher.script.revision=": %s' % scriptUsrVer)
    if scriptSysVer > scriptUsrVer:
        log('system scripts have been updated: %s > %s' % (scriptSysVer, scriptUsrVer))
        if dialog.yesno("Steam Launcher", "" + language(50124) + "", "" + language(50121) + "",
                        "" + language(50125) + ""):
            log('script updated dialog')
            addon.openSettings()
            delUserScriptSett = addon.getSetting("DelUserScript")
            if delUserScriptSett == 'true':
                log('option delUserScriptSett enabled: %s' % delUserScriptSett)
            elif delUserScriptSett == 'false':
                log('option delUserScriptSett disabled: %s' % delUserScriptSett)
        else:
            addon.setSetting(id="ScriptUpdateCheck", value="false")
            log('no selected, script update check disabled: ScriptUpdateCheck = %s' % scriptUpdateCheck)
    else:
        log('userdata script are up to date')


def quitXbmcDialog():
    global quitXbmcSetting
    if quitXbmcSetting == '2':
        log('quit setting: %s selected, asking user to pick' % quitXbmcSetting)
        if dialog.yesno("Steam Launcher", "" + language(50073) + ""):
            quitXbmcSetting = '0'
        else:
            quitXbmcSetting = '1'
    log('quit setting: %s selected' % quitXbmcSetting)


def xbmcBusyDialog():
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    log('busy dialog started')
    time.sleep(busyDialogTime)
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    log('busy dialog stopped after: %s seconds' % busyDialogTime)


def steamPrePost():
    global postScript
    global preScript
    if preScriptEnabled == 'false':
        preScript = 'false'
    elif preScript == '':
        preScript = 'false'
    log('pre steam script: %s' % preScript)
    if postScriptEnabled == 'false':
        postScript = 'false'
    elif postScript == '':
        postScript = 'false'
    log('post steam script: %s' % postScript)


def launchSteam():
    basePath = os.path.join(getAddonDataPath(), 'scripts')
    if osAndroid:
        cmd = "com.valvesoftware.android.steam.community"
        log('attempting to launch: "%s"' % cmd)
        xbmc.executebuiltin('XBMC.StartAndroidActivity("%s")' % cmd)
        xbmcBusyDialog()
        sys.exit()
    elif osWin:
        launchhidden = os.path.join(basePath, 'LaunchHidden.vbs')
        steamlauncher = os.path.join(basePath, 'SteamLauncher-AHK.exe')
        cmd = "\"" + launchhidden + "\"" + " " + "\"" + steamlauncher + "\"" + " " + "\"" + steamWin + "\"" + " " + "\"" + xbmcWin + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
    elif osOsx:
        steamlauncher = os.path.join(basePath, 'steam-launch.sh')
        cmd = "\"" + steamlauncher + "\"" + " " + "\"" + steamOsx + "\"" + " " + "\"" + xbmcOsx + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
    elif osLinux:
        steamlauncher = os.path.join(basePath, 'steam-launch.sh')
        cmd = "\"" + steamlauncher + "\"" + " " + "\"" + steamLinux + "\"" + " " + "\"" + xbmcLinux + "\"" + " " + "\"" + quitXbmcSetting + "\"" + " " + "\"" + xbmcPortable + "\"" + " " + "\"" + preScript + "\"" + " " + "\"" + postScript + "\""
    try:
        log('attempting to launch: %s' % cmd)
        subprocess.Popen(cmd, shell=True)
        xbmcBusyDialog()
    except:
        log('ERROR: failed to launch: %s' % cmd)
        scriptErrorNotification


log('****Running Steam-Launcher....')

if osAndroid:
    global osLinux
    osLinux = 0

log('running on osAndroid, osOsx, osLinux, os Win: %s %s %s %s ' % (osAndroid, osOsx, osLinux, osWin))

scriptVersionCheck()
usrScriptDelete()
copyLauncherScriptsToUserdata()
fileChecker()
makeScriptExec()
steamPrePost()
quitXbmcDialog()
launchSteam()