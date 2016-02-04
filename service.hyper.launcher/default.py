# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui
import os, random

scriptid = 'service.hyper.launcher'
HLaddonDataPath = xbmc.translatePath('special://profile/addon_data/plugin.hyper.launcher')
addon = xbmcaddon.Addon(id='service.hyper.launcher')
bg_video_wait_time = int(addon.getSetting("bg_video_wait_time"))
attract_wait_time = int(addon.getSetting("attract_wait_time"))
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
	addon_path = xbmc.getInfoLabel('Container.FolderPath')
	if 'plugin.hyper.launcher' in addon_path:
		idle_time = xbmc.getGlobalIdleTime()
		if bg_video_wait_time != 0:
			if idle_time > bg_video_wait_time:
				if not xbmc.Player().isPlayingVideo():
					xbmc.Player().play(item=xbmc.getInfoLabel('ListItem.Trailer'), windowed=1)
			else:
				if xbmc.Player().isPlayingVideo():
					xbmc.Player().stop()
		if attract_wait_time != 0:
			if idle_time > attract_wait_time:
				total_list_items = int(xbmc.getInfoLabel('Container(id).NumItems'))
				current_selection = int(xbmc.getInfoLabel('Container(id).CurrentItem'))
				win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
				cid = win.getFocusId()
				random_pool = range(1, current_selection) + range(current_selection + 1, total_list_items + 1)
				random_list_item = random.choice(random_pool)
				if xbmc.Player().isPlayingVideo():
					xbmc.Player().stop()
				xbmc.executebuiltin('SetFocus(%s, %s)' % (cid, int(random_list_item)))
				xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Input.ExecuteAction", "params": { "action": "noop"} }')
	xbmc.sleep(500)