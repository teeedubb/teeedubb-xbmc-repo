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
import xbmcvfs

addon = xbmcaddon.Addon(id='script.steam.launcher')
addonPath = addon.getAddonInfo('path')
addonIcon = addon.getAddonInfo('icon')
addonVersion = addon.getAddonInfo('version')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
scriptid = 'script.steam.launcher'

steamLinux = addon.getSetting("SteamLinux")
kodiLinux = addon.getSetting("KodiLinux")
steamWin = addon.getSetting("SteamWin")
kodiWin = addon.getSetting("KodiWin")
steamOsx = addon.getSetting("SteamOsx")
kodiOsx = addon.getSetting("KodiOsx")
delUserScriptSett = addon.getSetting("DelUserScript")
quitKodiSetting = addon.getSetting("QuitKodi")
busyDialogTime = int(addon.getSetting("BusyDialogTime"))
scriptUpdateCheck = addon.getSetting("ScriptUpdateCheck")
filePathCheck = addon.getSetting("FilePathCheck")
kodiPortable = addon.getSetting("KodiPortable")
preScriptEnabled = addon.getSetting("PreScriptEnabled")
preScript = addon.getSetting("PreScript")
postScriptEnabled = addon.getSetting("PostScriptEnabled")
postScript = addon.getSetting("PostScript")
osWin = xbmc.getCondVisibility('system.platform.windows')
osOsx = xbmc.getCondVisibility('system.platform.osx')
osLinux = xbmc.getCondVisibility('system.platform.linux')
osAndroid = xbmc.getCondVisibility('system.platform.android')
wmctrlCheck = addon.getSetting("WmctrlCheck")
suspendAudio = addon.getSetting("SuspendAudio")
customScriptFolder = addon.getSetting("CustomScriptFolder")
customScriptFolderEnabled = addon.getSetting("CustomScript")
minimiseKodi = addon.getSetting("MinimiseKodi")
steamParameters = addon.getSetting("SteamParameters")
forceKillKodi = addon.getSetting("ForceKillKodi")
desktopMode = addon.getSetting("DesktopMode")
androidApp = addon.getSetting("AndroidApp")

def log(msg):
	#msg = msg.encode(txt_encode)
	xbmc.log('%s: %s' % (scriptid, msg))

def getAddonInstallPath():
	path = addon.getAddonInfo('path')
	return path

def getAddonDataPath():
	path = xbmcvfs.translatePath('special://profile/addon_data/%s' % scriptid)
	if not os.path.exists(path):
		log('addon userdata folder does not exist, creating: %s' % path)
		try:
			os.makedirs(path)
			log('created directory: %s' % path)
		except:
			log('ERROR: failed to create directory: %s' % path)
			dialog.notification(language(50212), language(50125), addonIcon, 5000)
	return path

def copyLauncherScriptsToUserdata():
	oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
	if osWin:
		oldPath = os.path.join(oldBasePath, 'steam-launcher.ahk')
		newPath = os.path.join(scripts_path, 'steam-launcher.ahk')
		copyFile(oldPath, newPath)
		oldPath = os.path.join(oldBasePath, 'steam-launcher.exe')
		newPath = os.path.join(scripts_path, 'steam-launcher.exe')
		copyFile(oldPath, newPath)
	elif osLinux + osOsx:
		oldPath = os.path.join(oldBasePath, 'steam-launcher.sh')
		newPath = os.path.join(scripts_path, 'steam-launcher.sh')
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
			dialog.notification(language(50212), language(50125), addonIcon, 5000)
			sys.exit()
	if not os.path.isfile(newPath):
		log('script file does not exist, copying to userdata: %s' % newPath)
		try:
			shutil.copy2(oldPath, newPath)
			log('sucsessfully copied userdata script: %s' % newPath)
		except:
			log('ERROR: failed to copy script file to userdata: %s' % newPath)
			dialog.notification(language(50212), language(50125), addonIcon, 5000)
			sys.exit()
	else:
		log('script file already exists, skipping copy to userdata: %s' % newPath)

def makeScriptExec():
	scriptPath = os.path.join(scripts_path, 'steam-launcher.sh')
	if os.path.isfile(scriptPath):
		if '\r\n' in open(scriptPath,'r').read():
			log('Windows line endings found in %s, converting to unix line endings.' % scriptPath)
			with open(scriptPath, 'rb') as f:
				content = f.read()
				content = content.replace('\r\n', '\n')
			with open(scriptPath, 'wb') as f:
				f.write(content)
		if not stat.S_IXUSR & os.stat(scriptPath)[stat.ST_MODE]:
			log('steam-launcher.sh not executable: %s' % scriptPath)
			try:
				os.chmod(scriptPath, stat.S_IRWXU)
				log('steam-launcher.sh now executable: %s' % scriptPath)
			except:
				log('ERROR: unable to make steam-launcher.sh executable, exiting: %s' % scriptPath)
				dialog.notification(language(50212), language(50125), addonIcon, 5000)
				sys.exit()
			log('steam-launcher.sh executable: %s' % scriptPath)

def usrScriptDelete():
	if delUserScriptSett == 'true':
		log('deleting userdata scripts, option enabled: delUserScriptSett = %s' % delUserScriptSett)
		scriptFile = os.path.join(scripts_path, 'steam-launcher.ahk')
		delUserScript(scriptFile)
		scriptFile = os.path.join(scripts_path, 'steam-launcher.exe')
		delUserScript(scriptFile)
		scriptFile = os.path.join(scripts_path, 'steam-launcher.sh')
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
			dialog.notification(language(50212), language(50125), addonIcon, 5000)
		addon.setSetting(id="DelUserScript", value="false")

def fileChecker():
	if osLinux:
		if wmctrlCheck == 'true':
			if subprocess.call(["which", "wmctrl"]) != 0:
				log('ERROR: System program "wmctrl" not present, install it via you system package manager or if you are running the SteamOS compositor disable the addon option "Check for program wmctrl" (ONLY FOR CERTAIN USE CASES!!)')
				dialog.notification(language(50212), language(50125), addonIcon, 5000)
				sys.exit()
			else:
				log('wmctrl present, checking if a window manager is running...')
				display = None
				if 'DISPLAY' in os.environ: display = os.environ['DISPLAY'] # We inherited DISPLAY from Kodi, pass it down
				else:
					for var in open('/proc/%d/environ' % os.getppid()).read().split('\x00'):
						if var.startswith('DISPLAY='): display = var[8:] # Read DISPLAY from parent process if present
				if display is None or subprocess.call('DISPLAY=%s wmctrl -l' % display, shell=True) != 0:
					log('ERROR: A window manager is NOT running - unless you are using the SteamOS compositor Steam BPM needs a windows manager. If you are using the SteamOS compositor disable the addon option "Check for program wmctrl"')
					dialog.notification(language(50212), language(50125), addonIcon, 5000)
					sys.exit()
				else:
					log('A window manager is running...')
		if minimiseKodi == "true":
			if subprocess.call(["which", "xdotool"]) != 0:
				log('ERROR: Minimised Kodi enabled and system program "xdotool" not present, install it via you system package manager. Xdotool is required to minimise Kodi.')
				dialog.notification(language(50212), language(50125), addonIcon, 5000)
				sys.exit()
			else:
				log('xdotool present...')
	if filePathCheck == 'true':
		log('running program file check, option is enabled: filePathCheck = %s' % filePathCheck)
		if osWin:
			steamWin = addon.getSetting("SteamWin")
			kodiWin = addon.getSetting("KodiWin")
			steamExe = os.path.join(steamWin)
			xbmcExe = os.path.join(kodiWin)
			programFileCheck(steamExe, xbmcExe)
		elif osOsx:
			steamOsx = addon.getSetting("SteamOsx")
			kodiOsx = addon.getSetting("KodiOsx")
			steamExe = os.path.join(steamOsx)
			xbmcExe = os.path.join(kodiOsx)
			programFileCheck(steamExe, xbmcExe)
		elif osLinux:
			steamLinux = addon.getSetting("SteamLinux")
			kodiLinux = addon.getSetting("KodiLinux")
			steamExe = os.path.join(steamLinux)
			xbmcExe = os.path.join(kodiLinux)
			programFileCheck(steamExe, xbmcExe)
	else:
		log('skipping program file check, option disabled: filePathCheck = %s' % filePathCheck)

def fileCheckDialog(programExe):
	log('ERROR: dialog to go to addon settings because executable does not exist: %s' % programExe)
	if dialog.yesno(language(50212), programExe, language(50210), language(50211)):
		log('yes selected, opening addon settings')
		addon.openSettings()
		fileChecker()
		sys.exit()
	else:
		log('ERROR: no selected with invalid executable, exiting: %s' % programExe)
		sys.exit()

def programFileCheck(steamExe, xbmcExe):
	if osWin + osLinux:
		if os.path.isfile(os.path.join(steamExe)):
			log('Steam executable exists %s' % steamExe)
		else:
			fileCheckDialog(steamExe)
		if os.path.isfile(os.path.join(xbmcExe)):
			log('Xbmc executable exists %s' % xbmcExe)
		else:	
			fileCheckDialog(xbmcExe)
	if osOsx:
		if os.path.isdir(os.path.join(steamExe)):
			log('Steam folder exists %s' % steamExe)
		else:
			fileCheckDialog(steamExe)
		if os.path.isdir(os.path.join(xbmcExe)):
			log('Xbmc executable exists %s' % xbmcExe)
		else:	
			fileCheckDialog(xbmcExe)

def scriptVersionCheck():
	if scriptUpdateCheck == 'true':
		log('usr scripts are set to be checked for updates...')
		if delUserScriptSett == 'false':
			log('usr scripts are not set to be deleted, running version check')
			sysScriptDir = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
			if osWin:
				sysScriptPath = os.path.join(sysScriptDir, 'steam-launcher.ahk')
				usrScriptPath = os.path.join(scripts_path, 'steam-launcher.ahk')
				if os.path.isfile(os.path.join(usrScriptPath)):
					compareFile(sysScriptPath, usrScriptPath)
				else:
					log('usr script does not exist, skipping version check')
			elif osLinux + osOsx:
				sysScriptPath = os.path.join(sysScriptDir, 'steam-launcher.sh')
				usrScriptPath = os.path.join(scripts_path, 'steam-launcher.sh')
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
	scriptSysVer = '000'
	scriptUsrVer = '000'
	if os.path.isfile(sysScriptPath):
		with open(sysScriptPath, 'r') as f:
			for line in f.readlines():
				if "steam.launcher.script.revision=" in line:
					scriptSysVer = line[32:35]
		log('sys "steam.launcher.script.revision=": %s' % scriptSysVer)
	if os.path.isfile(usrScriptPath):
		with open(usrScriptPath, 'r') as f:
			for line in f.readlines():
				if "steam.launcher.script.revision=" in line:
					scriptUsrVer = line[32:35]
		log('usr "steam.launcher.script.revision=": %s' % scriptUsrVer)
	if scriptSysVer > scriptUsrVer:
		log('system scripts have been updated: sys:%s > usr:%s' % (scriptSysVer, scriptUsrVer))
		if dialog.yesno(language(50113), language(50213)):
			delUserScriptSett = 'true'
			log('yes selected, option delUserScriptSett enabled: %s' % delUserScriptSett)
		else:
			delUserScriptSett = 'false'
			log('no selected, script update check disabled: ScriptUpdateCheck = %s' % scriptUpdateCheck)
	else:
		log('userdata script are up to date')

def quitKodiDialog():
	global quitKodiSetting
	if quitKodiSetting == '2':
		log('quit setting: %s selected, asking user to pick' % quitKodiSetting)
		if dialog.yesno('Steam Launcher', language(50053)):
			quitKodiSetting = '0'
		else:
			quitKodiSetting = '1'
	if quitKodiSetting == '1' and minimiseKodi == "false":
		quitKodiSetting = '3'
	log('quit setting selected: %s' % quitKodiSetting)

def kodiBusyDialog():
	if busyDialogTime != 0:
		xbmc.executebuiltin("ActivateWindow(busydialognocancel)")
		log('busy dialog started')
		time.sleep(busyDialogTime)
		xbmc.executebuiltin("Dialog.Close(busydialognocancel)")
		log('busy dialog stopped after: %s seconds' % busyDialogTime)

def steamPrePost():
	global postScript
	global preScript
	if preScriptEnabled == 'false':
		preScript = 'false'
	elif preScriptEnabled == 'true':
		if not os.path.isfile(os.path.join(preScript)):
			log('pre-steam script does not exist, disabling: "%s"' % preScript)
			preScript = 'false'
			dialog.notification(language(50212), language(50214), addonIcon, 5000)
	elif preScript == '':
		preScript = 'false'
	log('pre steam script: %s' % preScript)
	if postScriptEnabled == 'false':
		postScript = 'false'
	elif postScriptEnabled == 'true':
		if not os.path.isfile(os.path.join(postScript)):
			log('post-steam script does not exist, disabling: "%s"' % postScript)
			postScript = 'false'
			dialog.notification(language(50212), language(50215), addonIcon, 5000)
	elif postScript == '':
		postScript = 'false'
	log('post steam script: %s' % postScript)

def launchSteam():
	if osAndroid:
		if androidApp == '0':
			cmd = "com.valvesoftware.android.steam.community"
		elif androidApp == '1':
			cmd = "com.valvesoftware.steamlink"
		log('attempting to launch: "%s"' % cmd)
		xbmc.executebuiltin('StartAndroidActivity("%s")' % cmd)
		kodiBusyDialog()
		sys.exit()
	elif osWin:
		steamlauncher = os.path.join(scripts_path, 'steam-launcher.exe')
		cmd = '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (steamlauncher, steamWin, kodiWin, quitKodiSetting, kodiPortable, preScript, postScript, steamParameters, forceKillKodi, desktopMode)
	elif osOsx:
		steamlauncher = os.path.join(scripts_path, 'steam-launcher.sh')
		cmd = '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (steamlauncher, steamOsx, kodiOsx, quitKodiSetting, kodiPortable, preScript, postScript, steamParameters, forceKillKodi, desktopMode)
	elif osLinux:
		steamlauncher = os.path.join(scripts_path, 'steam-launcher.sh')
		cmd = '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (steamlauncher, steamLinux, kodiLinux, quitKodiSetting, kodiPortable, preScript, postScript, steamParameters, forceKillKodi, desktopMode)
	try:
		log('attempting to launch: %s' % cmd)
#		print cmd.encode('utf-8')
		if suspendAudio == 'true':
			xbmc.audioSuspend()
			log('Audio suspended')
		if quitKodiSetting != '0' and suspendAudio == 'true':
			proc_h = subprocess.Popen(cmd, shell=True, close_fds=False)
			kodiBusyDialog()
			log('Waiting for Steam to exit')
			while proc_h.returncode is None:
				xbmc.sleep(1000)
				proc_h.poll()
			log('Start resuming audio....')
			xbmc.audioResume()
			log('Audio resumed')
			del proc_h		
		else:
			subprocess.Popen(cmd, shell=True, close_fds=True)
			kodiBusyDialog()
	except:
		log('ERROR: failed to launch: %s' % cmd)
#		print cmd.encode(txt_encode)
		dialog.notification(language(50212), language(50125), addonIcon, 5000)

#HACK: sys.getfilesystemencoding() is not supported on all systems (e.g. Android)
txt_encode = 'utf-8'
try:
	txt_encode = sys.getfilesystemencoding()
except:
	pass
#osAndroid returns linux + android
if osAndroid: 
	osLinux = 0
	txt_encode = 'utf-8'
log('****Running Steam-Launcher v%s....' % addonVersion)
log('running on osAndroid, osOsx, osLinux, osWin: %s %s %s %s ' % (osAndroid, osOsx, osLinux, osWin))
log('System text encoding in use: %s' % txt_encode)
if customScriptFolderEnabled == 'true':
	scripts_path = customScriptFolder
else:
	scripts_path = os.path.join(getAddonDataPath(), 'scripts')
scriptVersionCheck()
usrScriptDelete()
copyLauncherScriptsToUserdata()
fileChecker()
makeScriptExec()
steamPrePost()
quitKodiDialog()
launchSteam()
