import os, sys, re
import xbmcaddon
import subprocess
import xbmc, xbmcgui
import shutil, stat

# Shared resources
addonPath = ''
addon = xbmcaddon.Addon(id='script.steam.launcher')
addonPath = addon.getAddonInfo('path')

BASE_RESOURCE_PATH = os.path.join(addonPath, "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

steamLinux = addon.getSetting("SteamLinux")
xbmcLinux = addon.getSetting("XbmcLinux")
steamWin = addon.getSetting("SteamWin")
xbmcWin = addon.getSetting("XbmcWin")
delUserScript = addon.getSetting("DelUserScript")
makeShExec = addon.getSetting("MakeShExec")


from util import *
import util

def getAddonDataPath():
	path = ''
			
	path = xbmc.translatePath('special://profile/addon_data/%s' %(SCRIPTID))
		
	if not os.path.exists(path):
		try:
			os.makedirs(path)
		except:
			path = ''	
	return path


def getAddonInstallPath():
	path = ''
				
	path = __addon__.getAddonInfo('path')
	
	return path


def copyLauncherScriptsToUserdata():
	
	oldBasePath = os.path.join(util.getAddonInstallPath(), 'resources', 'scripts')
	newBasePath = os.path.join(util.getAddonDataPath(), 'scripts')
	
	if os.name == 'nt':
		pass # Windows
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
		pass
		oldPath = os.path.join(oldBasePath, 'steam-launch.sh')
		newPath = os.path.join(newBasePath, 'steam-launch.sh')
		copyScriptsFolder(newPath)
		copyFile(oldPath, newPath)
	
def copyFile(oldPath, newPath):
	newDir = os.path.dirname(newPath)
	if not os.path.isdir(newDir):
		try:
			os.mkdir(newDir)
			return
		except Exception, (exc):
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

basePath = os.path.join(util.getAddonDataPath(), 'scripts')			

if delUserScript == 'true':
	pass
	if os.name == 'nt':
		pass
		os.remove(os.path.join(basePath, 'SteamLauncher-AHK.ahk'))
		os.remove(os.path.join(basePath, 'SteamLauncher-AHK.exe'))
		os.remove(os.path.join(basePath, 'LaunchHidden.vbs'))
		addon.setSetting(id="DelUserScript", value="false")
	else:	
		pass
		os.remove(os.path.join(basePath, 'steam-launch.sh'))
		addon.setSetting(id="DelUserScript", value="false")
	
copyLauncherScriptsToUserdata()

if os.name == 'nt':
	pass # Windows
	precmd = os.path.join('cscript //B //Nologo', basePath, 'LaunchHidden.vbs')
	cmd = os.path.join(basePath, 'SteamLauncher-AHK.exe')
	if makeShExec == 'true':
		pass
		addon.setSetting(id="MakeShExec", value="false")
	subprocess.Popen(precmd+" "+"\""+cmd+"\""+" "+"\""+steamWin+"\""+" "+"\""+xbmcWin+"\"", shell=True)
else:
	pass # other (unix)
	cmd = os.path.join(basePath, 'steam-launch.sh')
	if makeShExec == 'true':
		pass
		os.chmod(cmd, stat.S_IRWXU)
		addon.setSetting(id="MakeShExec", value="false")
	subprocess.Popen(cmd+" "+"\""+steamLinux+"\""+" "+"\""+xbmcLinux+"\"", shell=True)