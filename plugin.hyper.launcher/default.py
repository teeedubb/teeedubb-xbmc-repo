# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import urllib
import urlparse
import os
import subprocess
import glob
import random
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

def log(msg, notification_msg):
	msg = msg.encode(txt_encode)
	xbmc.log('%s: %s' % (scriptid + '.log', msg))
	if 	notification_msg:
		dialog.notification('ERROR! Check log file...', notification_msg, addonIcon, 10000)
	
def file_check(file, required_file):
	if not file:
		file = required_file
	if not os.path.isfile(file):
		error_message = 'Required file does not exist "%s"' % file
		log(error_message, error_message)
		sys.exit()
		
def get_game_art(game_name, path, fallback_path):
#	search_item = os.path.join(path, game_name + '.*') #game_name + '.*'
#	search = glob.glob('%s' % search_item)
#	for filename in search:
#		return filename
#reminder that there is probably a better way to do this
	fanart = ''
	artwork = os.path.join(path, game_name + '.pdf')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(path, game_name + '.flv')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(path, game_name + '.avi')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(path, game_name + '.mp4')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(fallback_path, game_name + '.png')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(fallback_path, game_name + '.jpg')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(path, game_name + '.png')
	if os.path.isfile(artwork):
		fanart = artwork
	artwork = os.path.join(path, game_name + '.jpg')
	if os.path.isfile(artwork):
		fanart = artwork
	return fanart
	
def create_artwork_list(game_name, artwork_base_path):
	for folder in os.listdir(artwork_base_path):
		artwork = get_game_art(game_name, os.path.join(artwork_base_path, folder), 'none')
		if artwork:
			file_types = ['.png', '.jpg']
			if any(x in artwork for x in file_types):
				artwork_type = 'image'
			file_types = ['.mp4', '.avi', '.flv']
			if any(x in artwork for x in file_types):
				artwork_type = 'video'
			file_types = ['.pdf']
			if any(x in artwork for x in file_types):
				artwork_type = 'pdf'
			if artwork_type == 'pdf':
				li = xbmcgui.ListItem(folder, iconImage=os.path.join(addonPath, 'resources', 'media', 'pdf-artwork-icon.png'))
			else:
				li = xbmcgui.ListItem(folder, iconImage=artwork)
			li.setProperty('IsPlayable', 'false')
			url = build_url({ 'mode': 'artwork_display', 'artwork': artwork, 'artwork_type': artwork_type })
			if artwork_type == 'video':
				li.setProperty('IsPlayable', 'true')
				url = artwork
			xbmcplugin.addDirectoryItems(addon_handle, [(url, li, False)])
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

def emulator_launcher():
	selected_game = ''.join(args.get('filename'))
	launcher_script = ''.join(args.get('launcher_script'))
	rom_path = ''.join(args.get('rom_path'))
	folder_url = build_url({'mode': 'folder', 'foldername': ''.join(args.get('foldername'))})
	f = open(RESTART_FILE, 'w')
	f.write(folder_url)
	f.close()
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, ''.join(args.get('foldername')) + '-config.xml')
	tree = ET.parse(system_config)
	root = tree.getroot()
	for item in root.findall('alt_launchers'):
		for game in item.iter('game'):
			if ''.join(args.get('game_name')) in game.attrib['name']:
				launcher_script = game.find('launcher').text
	if selected_game: 
		search_item = os.path.join(rom_path, selected_game + '.*')
		search = glob.glob('%s' % search_item)
		if not search:
			file_check(''.join(search), search_item)
		for rom_full_path in search:
			rom_extension = os.path.splitext(rom_full_path)[1]
			rom_file = 	os.path.basename(rom_full_path)
		if launcher_script == 'kodi_retroplayer':
			listitem = xbmcgui.ListItem(rom_file, "0", "", "")
			parameters = {'Platform': ''.join(args.get('foldername')), 'Title': ''.join(args.get('game_name')), 'URL': rom_full_path}
			listitem.setInfo( type='game', infoLabels=parameters)
			xbmc.Player().play(rom_full_path, listitem)
		else:
			launcher_script_command = os.path.join(LAUNCHER_SCRIPTS, launcher_script)
			file_check(launcher_script_command, launcher_script_command)
			cmd = '"%s" "%s" "%s" "%s" "%s" "%s"' % (launcher_script_command, ''.join(args.get('foldername')), selected_game, rom_full_path, rom_file, rom_extension)
			log('Attempted command is:' , False)
			log(cmd, False)
			subprocess.Popen(cmd, shell=True, close_fds=True)
	
def search(system, search_string):
	system_name = system[:-4]
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	file_check(system_config, system_config)
	tree = ET.parse(system_config)
	root = tree.getroot()
	for item in root.findall('config'):
		rom_path = item.find('rom_path').text
		rom_extensions = item.find('rom_extensions').text
		launcher_script = item.find('launcher_script').text
	for item in root.findall('artwork'):
		artwork_base_path = item.find('base_path').text
		icon_path = item.find('icon').text
		icon_fallback_path = item.find('icon_fallback').text
		fanart_path = item.find('fanart').text
		fanart_fallback_path = item.find('fanart_fallback').text
		poster_path = item.find('poster').text
		thumb_path = item.find('thumb').text
		logo_path = item.find('logo').text
		clearart_path = item.find('clearart').text
		banner_path = item.find('banner').text
		media_path = item.find('media').text
		trailer_path = item.find('trailer').text
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system))
	root = tree.getroot()
	for game in root.findall('game'):
		game_description = game.find('description').text
		if search_string.lower() in game_description.lower():
			game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_two')
		
def game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, context_mode):
		game_name = game.find('description').text
		game_file_name = game.attrib['name']
		game_year = game.find('year').text
		game_manufacturer = game.find('manufacturer').text
		game_rating = game.find('rating').text
		game_genre = game.find('genre').text
		game_icon = get_game_art(game_name, icon_path, icon_fallback_path)
		game_fanart = get_game_art(game_name, fanart_path, fanart_fallback_path)
		game_thumb = get_game_art(game_name, thumb_path, 'none')
		game_poster = get_game_art(game_name, poster_path, 'none')
		game_logo = get_game_art(game_name, logo_path, 'none')
		game_clearart = get_game_art(game_name, clearart_path, 'none')
		game_banner = get_game_art(game_name, banner_path, 'none')
		game_media = get_game_art(game_name, media_path, 'none')
		game_trailer = get_game_art(game_name, trailer_path, 'trailer')
		url = build_url({'mode': 'file', 'foldername': system_name, 'game_name': game_name, 'filename': game_file_name, 'rom_path': rom_path, 'launcher_script': launcher_script, 'rom_extensions': rom_extensions})
		li = xbmcgui.ListItem(game_name, iconImage=game_icon)
		li.setProperty('mimetype', 'application/rom')
		li.setProperty('IsPlayable', 'false')
		li.setArt({ 'thumb': game_thumb, 'fanart': game_fanart, 'poster': game_poster, 'clearlogo': game_logo, 'clearart': game_clearart, 'banner': game_banner, 'discart': game_media })
		li.setInfo( 'video', { 'Title': game_name, 'OriginalTitle': game_file_name, 'Genre': game_genre, 'Year': game_year, 'Director': game_manufacturer, 'Mpaa': game_rating, 'Trailer': game_trailer, 'Plot': system_name, 'Studio': game_manufacturer, 'Path': rom_path, 'launcher_script': launcher_script } )
		contextMenuItems = []
		if context_mode != 'context_two':
			contextMenuItems.append(('Search this system', 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'system_name': system_name}) ,))
		contextMenuItems.append(('View artwork', 'XBMC.Container.Update(%s)' % build_url({'mode': 'artwork', 'game_name': game_name, 'artwork_base_path': artwork_base_path}) ,))
		contextMenuItems.append(('Random item', 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
		if context_mode == 'context_one':
			li.addContextMenuItems(contextMenuItems,  replaceItems=True)
		else:
			li.addContextMenuItems(contextMenuItems)
		xbmcplugin.addDirectoryItems(addon_handle, [(url, li, False)])

if addon_handle > 0:
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
		
if mode is None:
	for system in os.listdir(SYSTEMS_PATH):
		if system.endswith(".xml"):
			system_name = system[:-4]
			system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
			file_check(system_config, system_config)
			tree = ET.parse(system_config)
			root = tree.getroot()
			for item in root.findall('info'):
				release_year = item.find('release_year').text
				manufacturer = item.find('manufacturer').text
				description = item.find('description').text
			system_icon = get_game_art(system_name + '-icon', SYSTEMS_PATH, 'none')
			system_logo = get_game_art(system_name + '-logo', SYSTEMS_PATH, 'none')
			system_fanart = get_game_art(system_name + '-fanart', SYSTEMS_PATH, 'none')
			system_trailer = get_game_art(system_name + '-trailer', SYSTEMS_PATH, 'none')
			url = build_url({'mode': 'folder', 'foldername': system_name})
			li = xbmcgui.ListItem(system_name, iconImage=system_icon)
			li.setArt({ 'thumb': system_icon, 'fanart': system_fanart, 'clearlogo': system_logo })
			li.setInfo( 'video', { "Title": system_name, "Trailer": system_trailer, 'Year': release_year, 'Director': manufacturer, 'Plot': description } )
			li.setProperty('IsPlayable', 'false')
			contextMenuItems = []
			contextMenuItems.append(('Search all systems', 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'system_name': 'all'}) ,))
			contextMenuItems.append(('Random item', 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
			if system_trailer:
				contextMenuItems.append(('Play trailer', 'PlayMedia(%s)'  % (system_trailer) ,))
			if system_icon:
				contextMenuItems.append(('View icon', 'ShowPicture(%s)' % (system_icon) ,))
			if system_fanart:
				contextMenuItems.append(('View fanart', 'ShowPicture(%s)' % (system_fanart) ,))
			if system_logo:
				contextMenuItems.append(('View logo', 'ShowPicture(%s)'  % (system_logo) ,))
			li.addContextMenuItems(contextMenuItems)
			xbmcplugin.addDirectoryItems(addon_handle, [(url, li, True)])
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'folder':
	system_name = args['foldername'][0]
	system_game_list = args['foldername'][0] + '.xml'
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	tree = ET.parse(system_config)
	root = tree.getroot()
	for item in root.findall('config'):
		rom_path = item.find('rom_path').text
		rom_extensions = item.find('rom_extensions').text
		launcher_script = item.find('launcher_script').text
	for item in root.findall('artwork'):
		artwork_base_path = item.find('base_path').text
		icon_path = item.find('icon').text
		icon_fallback_path = item.find('icon_fallback').text
		fanart_path = item.find('fanart').text
		fanart_fallback_path = item.find('fanart_fallback').text
		poster_path = item.find('poster').text
		thumb_path = item.find('thumb').text
		logo_path = item.find('logo').text
		clearart_path = item.find('clearart').text
		banner_path = item.find('banner').text
		media_path = item.find('media').text
		trailer_path = item.find('trailer').text
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system_game_list))
	root = tree.getroot()
	for game in root.findall('game'):
		game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_one')
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'file':
	emulator_launcher()

elif mode[0] == 'search_input':
	search_string = dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	url = build_url({'mode': 'search', 'system_name': ''.join(args.get('system_name')), 'search_string': search_string})
	if len(search_string) == 0:
		log('Zero length search query', 'No search query entered')
	else:
		xbmc.executebuiltin('Container.Update(%s, refresh)' % url)
	
elif mode[0] == 'search':
	search_string = ''.join(args.get('search_string'))
	if ''.join(args.get('system_name')) == 'all':
		for system in os.listdir(SYSTEMS_PATH):
			if system.endswith('.xml'):
				search(system, search_string)
	else:
		system = ''.join(args.get('system_name')) + '.xml'
		search(system, search_string)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
	
elif mode[0] == 'artwork':
	game_name = ''.join(args.get('game_name'))
	artwork_base_path = ''.join(args.get('artwork_base_path'))
	create_artwork_list(game_name, artwork_base_path)

elif mode[0] == 'artwork_display':
#	if ''.join(args.get('artwork_type')) == 'video':
#		xbmc.Player().play(''.join(args.get('artwork')))
	if ''.join(args.get('artwork_type')) == 'image':
		xbmc.executebuiltin('ShowPicture("%s")' % (''.join(args.get('artwork'))))
	if ''.join(args.get('artwork_type')) == 'pdf':
		if not os.path.exists(xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')):
			log('special://home/addons/plugin.image.pdfreader/resources/lib not found, is plugin.image.pdfreader installed?', 'Is plugin.image.pdfreader installed?')
			sys.exit()
		pdf_url = 'plugin://plugin.image.pdfreader/' + '?' + urllib.urlencode({'mode': '1', 'url': ''.join(args.get('artwork')), 'name': ''.join(args.get('artwork'))})
		xbmc.executebuiltin('ActivateWindow(Pictures, %s, return)' % pdf_url)
		
elif mode[0] == 'random_focus':
	total_list_items = int(xbmc.getInfoLabel('Container(id).NumItems'))
	current_selection = int(xbmc.getInfoLabel('Container(id).CurrentItem'))
	win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	cid = win.getFocusId()
	random_pool = range(1, current_selection) + range(current_selection + 1, total_list_items + 1)
	if len(random_pool) > 0:
		random_list_item = random.choice(random_pool)
		if xbmc.Player().isPlayingVideo():
			xbmc.Player().stop()
		xbmc.executebuiltin('SetFocus(%s, %s)' % (cid, random_list_item))