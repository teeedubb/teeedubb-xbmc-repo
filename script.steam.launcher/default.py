 
#steam launcher by teeedubb. http://forum.xbmc.org/showthread.php?tid=157499
#I used Rom Collection Browser as a guide when making this addon, plus borrowed ideas and code from it too. Big thanks to malte for RCB!
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
steamOsx = addon.getSetting("SteamOsx")
xbmcOsx = addon.getSetting("XbmcOsx")
delUserScriptSett = addon.getSetting("DelUserScript")
makeShExec = addon.getSetting("MakeShExec")
makeShExecSett = addon.getSetting("MakeShExec")
quitXbmcSetting = addon.getSetting("QuitXbmc")
busyDialogTime = int(addon.getSetting("BusyDialogTime"))
scriptUpdateCheck = addon.getSetting("ScriptUpdateCheck")
filePathCheck = addon.getSetting("FilePathCheck")

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

def programFileCheck():
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.name == 'nt':
		if not os.path.isfile(os.path.join(steamWin)):
			if dialog.yesno(""+language(50123)+"", ""+steamWin+"", ""+language(50120)+"", ""+language(50121)+""): 
				addon.openSettings()
			else:
				sys.exit()
		if not os.path.isfile(os.path.join(xbmcWin)):
			if dialog.yesno(""+language(50123)+"", ""+xbmcWin+"", ""+language(50120)+"", ""+language(50121)+""): 
				addon.openSettings()
			else:
				sys.exit()
	else:
		if not os.path.isfile(os.path.join(steamLinux)):
			if dialog.yesno(""+language(50123)+"", ""+steamLinux+"", ""+language(50120)+"", ""+language(50121)+""): 
				addon.openSettings()
			else:
				sys.exit()
		if not os.path.isfile(os.path.join(xbmcLinux)):
			if dialog.yesno(""+language(50123)+"", ""+xbmcLinux+"", ""+language(50122)+"", ""+language(50121)+""): 
				addon.openSettings()
			else:
				sys.exit()
			
		if not stat.S_IXUSR & os.stat(os.path.join(basePath, 'steam-launch.sh'))[stat.ST_MODE]:
			if dialog.yesno(""+language(50123)+"", ""+os.path.join(basePath, 'steam-launch.sh')+"", ""+language(50122)+"", ""+language(50121)+""): 
				addon.openSettings()
			else:
				sys.exit()

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
		
def scriptVersionCheck():
	oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
	newBasePath = os.path.join(getAddonDataPath(), 'scripts')
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
				if dialog.yesno("Steam Launcher", ""+language(50124)+"", ""+language(50121)+"", ""+language(50125)+""): 
					addon.openSettings()
					delUserScriptSett = addon.getSetting("DelUserScript")
					if delUserScriptSett == 'true':
						delUserScript()
				else:
					addon.setSetting(id="ScriptUpdateCheck", value="1")
					exit

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
				if dialog.yesno("Steam Launcher", ""+language(50124)+"", ""+language(50121)+"", ""+language(50125)+""): 
					addon.openSettings()
					delUserScriptSett = addon.getSetting("DelUserScript")
					if delUserScriptSett == 'true':
						delUserScript()
				else:
					addon.setSetting(id="ScriptUpdateCheck", value="1")
					exit

def quitXbmcDialog():
	global quitXbmcSetting
	if quitXbmcSetting == '2':
		if dialog.yesno("Steam Launcher", ""+language(50073)+""): 
			quitXbmcSetting = '0'
		else:
			quitXbmcSetting = '1'
			
def launchSteam():
	makeShExec = addon.getSetting("MakeShExec")
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.name == 'nt':
		cmd = os.path.join('cscript //B //Nologo', basePath, 'LaunchHidden.vbs', basePath, 'SteamLauncher-AHK.exe')
		if makeShExec == 'true':
			addon.setSetting(id="MakeShExec", value="false")
		subprocess.Popen("\""+cmd+"\""+" "+"\""+steamWin+"\""+" "+"\""+xbmcWin+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		time.sleep(busyDialogTime)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	else:
		cmd = os.path.join(basePath, 'steam-launch.sh')
		if makeShExec == 'true':
			os.chmod(cmd, stat.S_IRWXU)
			addon.setSetting(id="MakeShExec", value="false")
		if sys.platform == "darwin":
			subprocess.Popen("\""+cmd+"\""+" "+"\""+steamOsx+"\""+" "+"\""+xbmcOsx+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
		else:
			subprocess.Popen("\""+cmd+"\""+" "+"\""+steamLinux+"\""+" "+"\""+xbmcLinux+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		time.sleep(busyDialogTime)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	

if scriptUpdateCheck == '0':
	scriptVersionCheck()

if delUserScriptSett == 'true':
	delUserScript()

copyLauncherScriptsToUserdata()

if filePathCheck == 'true':
	programFileCheck()

quitXbmcDialog()

launchSteam()