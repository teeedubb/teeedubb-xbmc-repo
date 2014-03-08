#steam launcher by teeedubb. http://forum.xbmc.org/showthread.php?tid=157499
#I used Rom Collection Browser as a guide when making this addon, plus borrowed ideas and code from it too. Big thanks to malte for RCB!
import os, sys, re, subprocess, time
import xbmcaddon, xbmc, xbmcgui
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
batchFileLauncher = addon.getSetting("BatchFileLauncher")

def log(msg):
    xbmc.log(u'%s: %s' % (SCRIPTID, msg))
	
def getAddonInstallPath():
	path = ''
				
	path = addon.getAddonInfo('path')
	
	return path
	
def getAddonDataPath():
	path = ''
			
	path = xbmc.translatePath('special://profile/addon_data/%s' %(SCRIPTID))
		
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
		if batchFileLauncher == 'true':
			oldPath = os.path.join(oldBasePath, 'steam-launch.bat')
			newPath = os.path.join(newBasePath, 'steam-launch.bat')
			copyFile(oldPath, newPath)
			
			oldPath = os.path.join(oldBasePath, 'LaunchHidden-bat.vbs')
			newPath = os.path.join(newBasePath, 'LaunchHidden-bat.vbs')
			copyFile(oldPath, newPath)
		else:
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
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.name == 'nt':
		global steamWin
		global xbmcWin
		steamWin = addon.getSetting("SteamWin")
		if not os.path.isfile(os.path.join(steamWin)):
   			log('file does not exist: %s' % steamWin)
			if dialog.yesno(""+language(50123)+"", ""+steamWin+"", ""+language(50120)+"", ""+language(50121)+""): 
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
			if dialog.yesno(""+language(50123)+"", ""+xbmcWin+"", ""+language(50120)+"", ""+language(50121)+""): 
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
				if dialog.yesno(""+language(50123)+"", ""+steamOsx+"", ""+language(50120)+"", ""+language(50121)+""): 
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
				if dialog.yesno(""+language(50123)+"", ""+xbmcOsx+"", ""+language(50120)+"", ""+language(50121)+""): 
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
				if dialog.yesno(""+language(50123)+"", ""+steamLinux+"", ""+language(50120)+"", ""+language(50121)+""): 
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
				if dialog.yesno(""+language(50123)+"", ""+xbmcLinux+"", ""+language(50122)+"", ""+language(50121)+""): 
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
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if not os.name == 'nt':
		if not stat.S_IXUSR & os.stat(os.path.join(basePath, 'steam-launch.sh'))[stat.ST_MODE]:
			log('steam-launch.sh is not executable')
			if dialog.yesno(""+language(50123)+"", ""+os.path.join(basePath, 'steam-launch.sh')+"", ""+language(50122)+"", ""+language(50121)+""): 
				log('opening addon settings')
				addon.openSettings()
			else:
				log('exiting')
				sys.exit()

def delUserScript():
	log('deleting user_data scripts')
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.path.isfile(os.path.join(basePath, 'LaunchHidden-bat.vbs')):
		filePath = os.path.join(basePath, 'LaunchHidden-bat.vbs')
		try:
			os.remove(filePath)
			log('found and deleting: %s' % filePath)
		except:
			log('deleting failed: %s' % filePath)
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
				log('addon scripts have been updated: %s' % scriptAhkSys > scriptAhkUsr)
				if dialog.yesno("Steam Launcher", ""+language(50124)+"", ""+language(50121)+"", ""+language(50125)+""): 
					addon.openSettings()
					delUserScriptSett = addon.getSetting("DelUserScript")
					if delUserScriptSett == 'true':
						log('deleting old userdata scripts')
						delUserScript()
				else:
					log('no selected, script update check disabled')
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
				log('addon scripts have been updated: %s' % scriptAhkSys > scriptAhkUsr)
				if dialog.yesno("Steam Launcher", ""+language(50124)+"", ""+language(50121)+"", ""+language(50125)+""): 
					addon.openSettings()
					delUserScriptSett = addon.getSetting("DelUserScript")
					if delUserScriptSett == 'true':
						log('deleting old userdata scripts')
						delUserScript()
				else:
					log('no selected, script update check disabled')
					addon.setSetting(id="ScriptUpdateCheck", value="1")
					exit

def quitXbmcDialog():
	global quitXbmcSetting
	if batchFileLauncher == 'false':
		if quitXbmcSetting == '2':
			if dialog.yesno("Steam Launcher", ""+language(50073)+""): 
				quitXbmcSetting = '0'
			else:
				quitXbmcSetting = '1'
			
def launchSteam():
	makeShExec = addon.getSetting("MakeShExec")
	basePath = os.path.join(getAddonDataPath(), 'scripts')
	if os.name == 'nt':
		precmd = os.path.join('cscript //B //Nologo', basePath, 'LaunchHidden.vbs')
		cmd = os.path.join(basePath, 'SteamLauncher-AHK.exe')
		if makeShExec == 'true':
			addon.setSetting(id="MakeShExec", value="false")
			log('steam-launch.sh doesnt exist in windows, option disabled')
		if batchFileLauncher == 'true':
			try:
				log('attempting to launch: %s' % 'cscript //B //Nologo "%appdata%/XBMC/userdata/addon_data/script.steam.launcher/scripts/launchhidden-bat.vbs" "%appdata%/XBMC/userdata/addon_data/script.steam.launcher/scripts/steam-launch.bat"')
				subprocess.Popen('cscript //B //Nologo "%appdata%/XBMC/userdata/addon_data/script.steam.launcher/scripts/launchhidden-bat.vbs" "%appdata%/XBMC/userdata/addon_data/script.steam.launcher/scripts/steam-launch.bat"', shell=True)
			except:
				log('failed to launch : %s' % 'cscript //B //Nologo "%appdata%/XBMC/userdata/addon_data/script.steam.launcher/scripts/launchhidden-bat.vbs" "%appdata%/XBMC/userdata/addon_data/script.steam.launcher/scripts/steam-launch.bat"')
		else:
			try:
				log('attempting to launch: %s' % precmd+" "+"\""+cmd+"\""+" "+"\""+steamWin+"\""+" "+"\""+xbmcWin+"\""+" "+"\""+quitXbmcSetting+"\"")
				subprocess.Popen(precmd+" "+"\""+cmd+"\""+" "+"\""+steamWin+"\""+" "+"\""+xbmcWin+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
			except:
				log('failed to run: %s' % precmd+" "+"\""+cmd+"\""+" "+"\""+steamWin+"\""+" "+"\""+xbmcWin+"\""+" "+"\""+quitXbmcSetting+"\"")
		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		time.sleep(busyDialogTime)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	else:
		cmd = os.path.join(basePath, 'steam-launch.sh')
		if makeShExec == 'true':
			os.chmod(cmd, stat.S_IRWXU)
			addon.setSetting(id="MakeShExec", value="false")
			log('steam-launch.sh should now be executable and the option disabled')
		if not stat.S_IXUSR & os.stat(os.path.join(basePath, 'steam-launch.sh'))[stat.ST_MODE]:
			log('steam-launch.sh is not executable, exiting')
			sys.exit()
		if sys.platform == "darwin":
			try:
				log('attempting to launch: %s' % "\""+cmd+"\""+" "+"\""+steamOsx+"\""+" "+"\""+xbmcOsx+"\""+" "+"\""+quitXbmcSetting+"\"")
				subprocess.Popen("\""+cmd+"\""+" "+"\""+steamOsx+"\""+" "+"\""+xbmcOsx+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
			except:
				log('failed to launch: %s' % "\""+cmd+"\""+" "+"\""+steamOsx+"\""+" "+"\""+xbmcOsx+"\""+" "+"\""+quitXbmcSetting+"\"")
		else:
			try:
				log('attempting to launch: %s' % "\""+cmd+"\""+" "+"\""+steamLinux+"\""+" "+"\""+xbmcLinux+"\""+" "+"\""+quitXbmcSetting+"\"")
				subprocess.Popen("\""+cmd+"\""+" "+"\""+steamLinux+"\""+" "+"\""+xbmcLinux+"\""+" "+"\""+quitXbmcSetting+"\"", shell=True)
			except:
				log('failed to launch: %s' % "\""+cmd+"\""+" "+"\""+steamLinux+"\""+" "+"\""+xbmcLinux+"\""+" "+"\""+quitXbmcSetting+"\"")

		xbmc.executebuiltin( "ActivateWindow(busydialog)" )
		time.sleep(busyDialogTime)
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	
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
	MakeShExecCheck()
	log('checking if steam-launch.sh is executable')

if filePathCheck == '0':
	log('running program file check')
	programFileCheck()
else:
	log('program file check disabled')

quitXbmcDialog()

log('running steam...')
log('steamLinux: %s' % steamLinux)
log('xbmcLinux: %s' % xbmcLinux)
log('steamWin: %s' % steamWin)
log('xbmcWin: %s' % xbmcWin)
log('steamOsx: %s' % steamOsx)
log('xbmcOsx: %s' % xbmcOsx)
log('delUserScriptSett: %s' % delUserScriptSett)
log('makeShExec: %s' % makeShExec)
log('makeShExecSett: %s' % makeShExecSett)
log('quitXbmcSetting: %s' % quitXbmcSetting)
log('busyDialogTime: %s' % busyDialogTime)
log('scriptUpdateCheck: %s' % scriptUpdateCheck)
log('filePathCheck: %s' % filePathCheck)
log('batchFileLauncher: %s' % batchFileLauncher)

launchSteam()