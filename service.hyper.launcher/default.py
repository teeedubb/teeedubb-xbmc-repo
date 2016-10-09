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
SUPRESS_VIDEO_FILE = os.path.join(HLaddonDataPath, 'suppress_video_file.txt')

if relaunch_previous_view == 'true':
	if os.path.exists(RESTART_FILE):
		f = open(RESTART_FILE, 'r')
		plugin_path = f.readline()
		f.close()
		xbmc.executebuiltin('xbmc.ActivateWindow(Videos,%s)' % plugin_path)
		os.remove(RESTART_FILE)

while not xbmc.abortRequested:
	addon_path = xbmc.getInfoLabel('Container.FolderPath')
	if 'plugin.hyper.launcher' in addon_path and xbmc.getInfoLabel('System.CurrentWindow') == 'Videos' and '&mode=artwork&' not in addon_path and xbmc.translatePath('special://temp/plugin.hyper.launcher') not in addon_path and os.path.exists(SUPRESS_VIDEO_FILE) == False:
		idle_time = xbmc.getGlobalIdleTime()
		if bg_video_wait_time != 0 and idle_time > bg_video_wait_time:
			if xbmc.getInfoLabel('ListItem.Trailer') != 'False' and not xbmc.Player().isPlayingVideo():
				xbmc.Player().play(item=xbmc.getInfoLabel('ListItem.Trailer'), windowed=1)
		else:
			if xbmc.Player().isPlayingVideo():
				xbmc.Player().stop()
		if attract_wait_time != 0 and idle_time > attract_wait_time:
			total_list_items = int(xbmc.getInfoLabel('Container(id).NumItems'))
			current_selection = int(xbmc.getInfoLabel('Container(id).CurrentItem'))
			win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
			cid = win.getFocusId()
			random_pool = range(1, current_selection) + range(current_selection + 1, total_list_items + 1)
#			print('tli', total_list_items)
#			print('cli', current_selection, xbmc.getInfoLabel('ListItem.Title'))
#			print('rpoo', random_pool)
			if len(random_pool) > 0:
				random_listi = random.choice(random_pool)
				random_list_item = (random_listi - current_selection)
#				print('rli', random_list_item)
#				print('cid + rlii', cid, int(random_listi))
				xbmc.executebuiltin('SetFocus(%s, %s)' % (cid, 1))
				xbmc.executebuiltin('Control.Move(%s, %s)' % (cid, random_list_item))
				if xbmc.Player().isPlayingVideo():
					xbmc.Player().stop()
			xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Input.ExecuteAction", "params": { "action": "noop"} }')
	xbmc.sleep(250)
#	print('cli2', xbmc.getInfoLabel('Container(id).CurrentItem'), xbmc.getInfoLabel('ListItem.Title'))


