#steam launcher by teeedubb. 
import os, sys, re, subprocess, time
import xbmcaddon,  xbmc, xbmcgui
import shutil, stat

addonPath = ''
addon = xbmcaddon.Addon(id='script.steam.launcher')
addonPath = addon.getAddonInfo('path')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
SCRIPTID = 'script.steam.launcher'

steamLinux = addon.getSetting("SteamLinux")
xbmcLinux = addon.getSetting("XbmcLinux")
steamWin = addon.getSetting("SteamWin")
xbmcWin = addon.getSetting("XbmcWin")
delUserScriptSett = addon.getSetting("DelUserScript")
makeShExec = addon.getSetting("MakeShExec")
makeShExecSett = addon.getSetting("MakeShExec")
quitXbmcSetting = addon.getSetting("QuitXbmc")
busyDialogTime = int(addon.getSetting("BusyDialogTime"))

def getAddonInstallPath():
	path = ''
				
	path = addon.getAddonInfo('path')
	
	return path
	
def getAddonDataPath():
	path = ''
			
	path = xbmc.translatePath('special://profile/addon_data/%s' %(SCRIPTID))
		
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except:
			path = ''	
	return path

def copyLauncherScriptsToUserdata():
	
	oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
	newBasePath = os.path.join(getAddonDataPath(), 'scripts')
	
	if os.name == 'nt':
		oldPath = os.path.join(oldBasePath, 'SteamLauncher-AHK.ahk')
		newPath = os.path.join(newBasePath, 'SteamLauncher-AHK.ahk')
		copyScriptsFolder(newPath)
		copyFile(oldPath, newPath)
	
		oldPath = os.path.join(oldBasePath, 'SteamLauncher-AHK.exe')
		newPath = os.path.join(newBasePath, 'SteamLauncher-AHK.exe')
		copyFile(oldPath, newPath)
	
		oldPath = os.path.join(oldBasePath, 'LaunchHidden.vbs')
		newPath = os.path.join(newBasePath, 'LaunchHidden.vbs')
		copyFile(oldPath, newPath)
	else:	
		oldPath = os.path.join(oldBasePath, 'steam-launch.sh')
		newPath = os.path.join(newBasePath, 'steam-launch.sh')
		copyScriptsFolder(newPath)
		copyFile(oldPath, newPath)
	
def copyFile(oldPath, newPath):
	newDir = os.path.dirname(newPath)
	if not os.path.isdir(newDir):
		try:
			os.mkdir(newDir)
		except:
			return
	
	if not os.path.isfile(newPath):
		try:
			shutil.copy2(oldPath, newPath)
		except:
			return

def copyScriptsFolder(newPath):
	newDir = os.path.dirname(newPath)
	if not os.path.isdir(newDir):
		try:
			os.mkdir(newDir)
		except:
			return

def delUserScript():
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.name == 'nt':
		if os.path.isfile(os.path.join(basePath, 'SteamLauncher-AHK.ahk')):
			os.remove(os.path.join(basePath, 'SteamLauncher-AHK.ahk'))
		if os.path.isfile(os.path.join(basePath, 'SteamLauncher-AHK.exe')):
			os.remove(os.path.join(basePath, 'SteamLauncher-AHK.exe'))
		if os.path.isfile(os.path.join(basePath, 'LaunchHidden.vbs')):
			os.remove(os.path.join(basePath, 'LaunchHidden.vbs'))
		addon.setSetting(id="DelUserScript", value="false")
	else:
		if os.path.isfile(os.path.join(basePath, 'steam-launch.sh')):
			os.remove(os.path.join(basePath, 'steam-launch.sh'))
		addon.setSetting(id="DelUserScript", value="false")
		
def quitXbmcDialog():
	global quitXbmcSetting
	if os.name == 'nt':
		if quitXbmcSetting == '2':
			if dialog.yesno("Steam Launcher", ""+language(50073)+""): 
				quitXbmcSetting = '0'
			else:
				quitXbmcSetting = '1'
			
def launchSteam():
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.name == 'nt':
		precmd = os.path.join('cscript //B //Nologo', basePath, 'LaunchHidden.vbs')
		cmd = os.path.join(basePath, 'SteamLauncher-AHK.exe')
		if makeShExec == 'true':
			addon.setSetting(id="MakeShExec", value="false")
		subprocess.Popen(precmd+" "+"\""+cmd+"\""+" "+"\""+steamWin+"\""+" "+"\""+xbmcWin+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		time.sleep(busyDialogTime)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	else:
		cmd = os.path.join(basePath, 'steam-launch.sh')
		if makeShExec == 'true':
			os.chmod(cmd, stat.S_IRWXU)
			addon.setSetting(id="MakeShExec", value="false")
		subprocess.Popen(cmd+" "+"\""+steamLinux+"\""+" "+"\""+xbmcLinux+"\"", shell=True)
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		time.sleep(busyDialogTime)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	
if delUserScriptSett == 'true':
	delUserScript()

copyLauncherScriptsToUserdata()

quitXbmcDialog()

launchSteam()