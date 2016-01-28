# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import os
import sys
import subprocess
import shutil
import glob
import xml.etree.ElementTree as ET

scriptid = 'plugin.hyper.launcher'
addon = xbmcaddon.Addon(id='plugin.hyper.launcher')
addonPath = addon.getAddonInfo('path').decode("utf-8")
addonDataPath = xbmc.translatePath('special://profile/addon_data/%s' % scriptid).decode("utf-8")
addonIcon = addon.getAddonInfo('icon')
addonVersion = addon.getAddonInfo('version')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString

#addon paths
SYSTEMS_PATH = os.path.join(addonDataPath, 'systems')
SYSTEMS_CONFIG_PATH = os.path.join(addonDataPath, 'systems_config')
LAUNCHER_SCRIPTS = os.path.join(addonDataPath, 'launcher_scripts')
RESTART_FILE = os.path.join(addonDataPath, 'restart_file.txt')

#create addon paths
if not os.path.exists(addonDataPath): 
	os.makedirs(addonDataPath)
if not os.path.exists(SYSTEMS_PATH): 
	os.makedirs(SYSTEMS_PATH)
if not os.path.exists(SYSTEMS_CONFIG_PATH): 
	os.makedirs(SYSTEMS_CONFIG_PATH)
if not os.path.exists(LAUNCHER_SCRIPTS): 
	os.makedirs(LAUNCHER_SCRIPTS)

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)

txt_encode = 'utf-8'
try:
	txt_encode = sys.getfilesystemencoding()
except:
	pass
	
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def error_notification(msg):
	dialog.notification('ERROR! Check log file...', msg, addonIcon, 10000)
	
def log(msg):
	msg = msg.encode(txt_encode)
	xbmc.log('%s: %s' % (scriptid, msg))

def file_check(file, required_file):
	if not file:
		file = required_file
	if not os.path.isfile(file):
		error_message = 'Required file does not exist "%s"' % file
		log(error_message)
		error_notification(error_message)
		sys.exit()
		
def get_game_art(game_name, path1, path2, path3, path4):
#	search_item = os.path.join(path, game_name + '.*') #game_name + '.*'
#	search = glob.glob('%s' % search_item)
#	for filename in search:
#		return filename
	fanart = ''
	if path4 == 'trailer':
		artwork = os.path.join(path1, game_name + '.flv')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path1, game_name + '.avi')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path1, game_name + '.mp4')
		if os.path.isfile(artwork):
			fanart = artwork
	else:
		artwork = os.path.join(path4, game_name + '.png')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path4, game_name + '.jpg')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path3, game_name + '.png')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path3, game_name + '.jpg')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path2, game_name + '.png')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path2, game_name + '.jpg')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path1, game_name + '.png')
		if os.path.isfile(artwork):
			fanart = artwork
		artwork = os.path.join(path1, game_name + '.jpg')
		if os.path.isfile(artwork):
			fanart = artwork
	return fanart

def emulator_launcher():
	selected_game = ''.join(args.get('filename'))
	rom_path = ''.join(args.get('rom_path'))
	folder_url = build_url({'mode': 'folder', 'foldername': ''.join(args.get('foldername'))})
	f = open(RESTART_FILE, 'w')
	f.write(folder_url)
	f.close()
	if selected_game: 
		search_item = os.path.join(rom_path, selected_game + '.*')
		search = glob.glob('%s' % search_item)
		if not search:
			file_check(''.join(search), search_item)
		for rom_full_path in search:
			rom_extension = os.path.splitext(rom_full_path)[1]
			rom_file = 	os.path.basename(rom_full_path)
		if xbmc.getInfoLabel('ListItem.Writer') == 'kodi_retroplayer':
			print('kodi_retroplayer')
			XBMC.PlayMedia(rom_full_path)
		else:
			launcher_script_command = os.path.join(LAUNCHER_SCRIPTS, ''.join(args.get('launcher_script')))
			cmd = '"%s" "%s" "%s" "%s" "%s" "%s"' % (launcher_script_command, ''.join(args.get('foldername')), selected_game, rom_full_path, rom_file, rom_extension)
			log('Attempted command is:')
			print(cmd)
			subprocess.Popen(cmd, shell=True, close_fds=True)
	
def search(system, search_string):
	system_name = system[:-4]
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	file_check(system_config, system_config)
	tree = ET.parse(system_config)
	root = tree.getroot()
	rom_path = root.find('rom_path').text
	icon_path1 = root.find('icon_path1').text
	icon_path2 = root.find('icon_path2').text
	icon_path3 = root.find('icon_path3').text
	icon_path4 = root.find('icon_path4').text
	fanart_path1 = root.find('fanart_path1').text
	fanart_path2 = root.find('fanart_path2').text
	fanart_path3 = root.find('fanart_path3').text
	fanart_path4 = root.find('fanart_path4').text
	logo_path = root.find('logo_path').text
	trailer_path = root.find('trailer_path').text
	launcher_script = os.path.join(LAUNCHER_SCRIPTS, root.find('launcher_script').text)
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system))
	root = tree.getroot()
	for game in root.findall('game'):
		game_description = game.find('description').text
		if search_string in game_description.lower():
			game_year = game.find('year').text
			game_manufacturer = game.find('manufacturer').text
			game_rating = game.find('rating').text
			game_genre = game.find('genre').text
			game_name = game.attrib['name']
			game_icon = get_game_art(game_name, icon_path1, icon_path2, icon_path3, icon_path4)
			game_fanart = get_game_art(game_name, fanart_path1, fanart_path2, fanart_path3, fanart_path4)
			game_logo = get_game_art(game_name, logo_path, 'none', 'none', 'none')
			game_trailer = get_game_art(game_name, trailer_path, 'none', 'none', 'trailer')
			url = build_url({'mode': 'file', 'foldername': system_name, 'game_name': game_name, 'filename': game_description, 'rom_path': rom_path, 'launcher_script': launcher_script})
			li = xbmcgui.ListItem(game_description, iconImage=game_icon)
			li.setArt({ 'thumb': game_icon, 'fanart': game_fanart, 'clearlogo': game_logo })
			li.setInfo( 'video', { "Title": game_description, "OriginalTitle": game_name, "Genre": game_genre, "Year": game_year, "Director": game_manufacturer, "Mpaa": game_rating, "Plot": system_name, "Studio": rom_path, "Writer": launcher_script, "Trailer": game_trailer } )
			li.setProperty('IsPlayable', 'false')
			contextMenuItems = []
			if game_trailer:
				contextMenuItems.append(('Play game trailer', 'PlayMedia(%s)'  % (game_trailer) ,))
			if game_icon:
				contextMenuItems.append(('View game icon', 'ShowPicture(%s)' % (game_icon) ,))
			if game_fanart:
				contextMenuItems.append(('View game fanart', 'ShowPicture(%s)' % (game_fanart) ,))
			if game_logo:
				contextMenuItems.append(('View game logo', 'ShowPicture(%s)'  % (game_logo) ,))
			li.addContextMenuItems(contextMenuItems)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	
if addon_handle > 0:
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
		
if mode is None:
	for system in os.listdir(SYSTEMS_PATH):
		if system.endswith(".xml"):
			system_name = system[:-4]
			system_icon = get_game_art(system_name + '-icon', SYSTEMS_PATH, 'none', 'none', 'none')
			system_logo = get_game_art(system_name + '-logo', SYSTEMS_PATH, 'none', 'none', 'none')
			system_fanart = get_game_art(system_name + '-fanart', SYSTEMS_PATH, 'none', 'none', 'none')
			system_trailer = get_game_art(system_name + '-trailer', SYSTEMS_PATH, 'none', 'none', 'trailer')
			url = build_url({'mode': 'folder', 'foldername': system_name})
			li = xbmcgui.ListItem(system_name, iconImage=system_icon)
			li.setArt({ 'thumb': system_icon, 'fanart': system_fanart, 'clearlogo': system_logo })
			li.setInfo( 'video', { "Title": system_name, "Trailer": system_trailer } )
			li.setProperty('IsPlayable', 'false')
			contextMenuItems = []
			contextMenuItems.append(('Search all systems', 'xbmc.ActivateWindow(Videos,%s)' % build_url({'mode': 'search'}) ,))
			if system_trailer:
				contextMenuItems.append(('Play trailer', 'PlayMedia(%s)'  % (system_trailer) ,))
			if system_icon:
				contextMenuItems.append(('View icon', 'ShowPicture(%s)' % (system_icon) ,))
			if system_fanart:
				contextMenuItems.append(('View fanart', 'ShowPicture(%s)' % (system_fanart) ,))
			if system_logo:
				contextMenuItems.append(('View logo', 'ShowPicture(%s)'  % (system_logo) ,))
			li.addContextMenuItems(contextMenuItems)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'folder':
	system_name = args['foldername'][0]
	system_game_list = args['foldername'][0] + '.xml'
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	file_check(system_config, system_config)
	tree = ET.parse(system_config)
	root = tree.getroot()
	rom_path = root.find('rom_path').text
	icon_path1 = root.find('icon_path1').text
	icon_path2 = root.find('icon_path2').text
	icon_path3 = root.find('icon_path3').text
	icon_path4 = root.find('icon_path4').text
	fanart_path1 = root.find('fanart_path1').text
	fanart_path2 = root.find('fanart_path2').text
	fanart_path3 = root.find('fanart_path3').text
	fanart_path4 = root.find('fanart_path4').text
	logo_path = root.find('logo_path').text
	trailer_path = root.find('trailer_path').text
	launcher_script = os.path.join(LAUNCHER_SCRIPTS, root.find('launcher_script').text)
	file_check(launcher_script, launcher_script)
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system_game_list))
	root = tree.getroot()
	for game in root.findall('game'):
		game_description = game.find('description').text
		game_year = game.find('year').text
		game_manufacturer = game.find('manufacturer').text
		game_rating = game.find('rating').text
		game_genre = game.find('genre').text
		game_name = game.attrib['name']
		game_icon = get_game_art(game_name, icon_path1, icon_path2, icon_path3, icon_path4)
		game_fanart = get_game_art(game_name, fanart_path1, fanart_path2, fanart_path3, fanart_path4)
		game_logo = get_game_art(game_name, logo_path, 'none', 'none', 'none')
		game_trailer = get_game_art(game_name, trailer_path, 'none', 'none', 'trailer')
		url = build_url({'mode': 'file', 'foldername': system_name, 'game_name': game_name, 'filename': game_description, 'rom_path': rom_path, 'launcher_script': launcher_script})
		li = xbmcgui.ListItem(game_description, iconImage=game_icon)
		li.setProperty('IsPlayable', 'false')
		li.setArt({ 'thumb': game_icon, 'fanart': game_fanart, 'clearlogo': game_logo })
		li.setInfo( 'video', { "Title": game_description, "OriginalTitle": game_name, "Genre": game_genre, "Year": game_year, "Director": game_manufacturer, "Mpaa": game_rating, "Plot": system_name, "Studio": rom_path, "Writer": launcher_script, "Trailer": game_trailer } )
		contextMenuItems = []
		contextMenuItems.append(('Search this system', 'xbmc.ActivateWindow(Videos,%s)' % build_url({'mode': 'search', 'system_name': system_name}) ,)) #% (base_url, system_name) ,))
		if game_trailer:
			contextMenuItems.append(('Play game trailer', 'PlayMedia(%s)'  % (game_trailer) ,))
		if game_icon:
			contextMenuItems.append(('View game icon', 'ShowPicture(%s)' % (game_icon) ,))
		if game_fanart:
			contextMenuItems.append(('View game fanart', 'ShowPicture(%s)' % (game_fanart) ,))
		if game_logo:
			contextMenuItems.append(('View game logo', 'ShowPicture(%s)'  % (game_logo) ,))
		li.addContextMenuItems(contextMenuItems,  replaceItems=True)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'file':
	emulator_launcher()

elif mode[0] == 'search':
	search_string = dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	xbmc.executebuiltin("ActivateWindow(busydialog)")
	if args.get('system_name'):
		system = ''.join(args.get('system_name')) + '.xml'
		search(system, search_string)
	else:
		for system in os.listdir(SYSTEMS_PATH):
			if system.endswith('.xml'):
				search(system, search_string)		
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
	xbmc.executebuiltin("Dialog.Close(busydialog)")
		