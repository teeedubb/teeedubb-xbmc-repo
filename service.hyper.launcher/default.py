# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui
import os

scriptid = 'service.hyper.launcher'
HLaddonDataPath = xbmc.translatePath('special://profile/addon_data/plugin.hyper.launcher')
addon = xbmcaddon.Addon(id='service.hyper.launcher')
wait_time = int(addon.getSetting("wait_time"))
relaunch_previous_view = addon.getSetting("relaunch_previous_view")
RESTART_FILE = os.path.join(HLaddonDataPath, 'restart_file.txt')

if relaunch_previous_view == 'true':
	if os.path.exists(RESTART_FILE):
		f = open(RESTART_FILE, 'r')
		plugin_path = f.readline()
		xbmc.executebuiltin('xbmc.ActivateWindow(Videos,%s)' % plugin_path)
		f.close()
		os.remove(RESTART_FILE)


while not xbmc.abortRequested:
	if wait_time != 0:
		addon_path = xbmc.getInfoLabel('Container.FolderPath')
		idle_time = xbmc.getGlobalIdleTime()
		if 'plugin.hyper.launcher' in addon_path:
			if idle_time > wait_time:
				if not xbmc.Player().isPlayingVideo():
					xbmc.Player().play(item=xbmc.getInfoLabel('ListItem.Trailer'), windowed=1)
			else:
				if xbmc.Player().isPlayingVideo():
					xbmc.Player().stop()
	xbmc.sleep(500)