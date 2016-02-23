# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
import threading
import xml.etree.ElementTree as ET

#set text encoding.... ugh...
try:
	txt_encode = sys.getfilesystemencoding()
except:
	txt_encode = 'utf-8'
reload(sys)  
sys.setdefaultencoding('utf-8')

scriptid = 'plugin.hyper.launcher'
addon = xbmcaddon.Addon(id='plugin.hyper.launcher')
addonPath = addon.getAddonInfo('path')
addonDataPath = xbmc.translatePath('special://profile/addon_data/%s' % scriptid)
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

if addon_handle > 0:
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING)
	xbmcplugin.addSortMethod(handle=addon_handle, sortMethod=xbmcplugin.SORT_METHOD_STUDIO)

def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

def log(msg, notification_msg):
	xbmc.log('%s: %s' % (scriptid + '.log', msg))
	if 	notification_msg:
		dialog.notification(language(50103), notification_msg, addonIcon, 10000)

def file_check(file, required_file):
	if not file:
		file = required_file
	if not os.path.isfile(file):
		log_message = language(50102) + ': "%s"' % file
		log(log_message, log_message)
		sys.exit()
		
def get_game_art(game_file_name, path, fallback_path, type):
	fanart = ''
	if type == 'video':
		fanart_file_types = ('.flv', '.avi', '.mp4')
	elif type == 'image':
		fanart_file_types = ('.ico', '.png', '.jpg')
	else:
		fanart_file_types = ('.flv', '.avi', '.mp4', '.ico', '.png', '.jpg', '.mp3', '.pdf')
	for fanart_file_type in fanart_file_types:
		if not fallback_path == 'none':
			artwork = os.path.join(fallback_path, game_file_name + fanart_file_type)
			if os.path.isfile(artwork):
				return artwork
		artwork = os.path.join(path, game_file_name + fanart_file_type)
		if os.path.isfile(artwork):
			return artwork
			break
	
def get_system_info(system_config):
	tree = ET.parse(system_config)
	root = tree.getroot()
	for item in root.findall('config'):
		if not item.find('rom_path').text:
			log_message = language(50105) + ': %s, %s' % (system_config, 'rom_path')
			log(log_message, language(50105))
		else:
			rom_path = item.find('rom_path').text
		if item.find('rom_extensions').text:
			rom_extensions = item.find('rom_extensions').text
		else:
			rom_extensions = ''
		if not item.find('launcher_script').text:
			log_message = language(50105) + ': %s, %s' % (system_config, 'launcher_script')
			log(log_message, language(50105))
		else:
			launcher_script = item.find('launcher_script').text
	for item in root.findall('artwork'):
		if item.find('base_path').text:
			artwork_base_path = item.find('base_path').text
		else:
			artwork_base_path = ''
		if item.find('icon').text:
			icon_path = item.find('icon').text
		else:
			icon_path = ''
		if item.find('icon_fallback').text:
			icon_fallback_path = item.find('icon_fallback').text
		else:
			icon_fallback_path = ''
		if item.find('fanart').text:
			fanart_path = item.find('fanart').text
		else:
			fanart_path = ''
		if item.find('fanart_fallback').text:
			fanart_fallback_path = item.find('fanart_fallback').text
		else:
			fanart_fallback_path = ''
		if item.find('poster').text:
			poster_path = item.find('poster').text
		else:
			poster_path = ''
		if item.find('thumb').text:
			thumb_path = item.find('thumb').text
		else:
			thumb_path = ''
		if item.find('logo').text:
			logo_path = item.find('logo').text
		else:
			logo_path = ''
		if item.find('clearart').text:
			clearart_path = item.find('clearart').text
		else:
			clearart_path = ''
		if item.find('banner').text:
			banner_path = item.find('banner').text
		else:
			banner_path = ''
		if item.find('media').text:
			media_path = item.find('media').text
		else:
			media_path = ''
		if item.find('trailer').text:
			trailer_path = item.find('trailer').text
		else:
			trailer_path = ''
		return (rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path)
	
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
	if selected_game:
		for item in root.findall('game_variations'):
			for game in item.iter('game'):
				if ''.join(args.get('game_name')) in game.attrib['name']:
					if os.path.exists(os.path.join(rom_path, selected_game)):
						game_variation_list = []
						game_variation_list.append( selected_game, )
						for game_variation in os.listdir(os.path.join(rom_path, selected_game)):
							game_variation_list.append( os.path.splitext(game_variation)[0], )
						selected_var_game = dialog.select(language(50200), game_variation_list)
						if selected_var_game == -1:
							sys.exit()
						elif selected_var_game == 0:
							break
						else:
							selected_var_game = game_variation_list[selected_var_game]
						rom_path = os.path.join(rom_path, selected_game)
						selected_game = selected_var_game
						if not args.get('alt_launcher'):
							if game.find('launcher').text:
								launcher_script = game.find('launcher').text
					else:
						log_message = language(50109) + os.path.join(rom_path, selected_game)
						log(log_message, language(50109))
		if not args.get('alt_launcher'):
			for item in root.findall('alt_launchers'):
				for game in item.iter('game'):
					if selected_game in game.attrib['name']:
						launcher_script = game.find('launcher').text
		if not args.get('rom_extensions'): # == 'none':
			search_item = os.path.join(rom_path, selected_game + '.*')
			rom_full_path = ''.join(glob.glob('%s' % search_item))
		else:
			file_types = []
			file_types = ''.join(args.get('rom_extensions')).split(' ')
			for file_type in file_types:
				file_type = '.' + file_type
				rom_full_path = os.path.join(rom_path, selected_game) + file_type
				if os.path.isfile(rom_full_path):
					break
		if not rom_full_path:
			file_check(''.join(search_item), search_item)
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
			log(language(50104), False)
			log(cmd, False)
			subprocess.Popen(cmd.encode(txt_encode), shell=True, close_fds=True)
	else:
		log(language(50110), language(50110))

def search(system, search_string):
	system_name = system[:-4]
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	file_check(system_config, system_config)
	log_message = 'Reading: %s' % system_config
	log(log_message, False)
	rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path = get_system_info(system_config)
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system))
	root = tree.getroot()
	for game in root.findall('game'):
		game_description = game.find('description').text
		if search_string != False:
			if search_string.lower() in game_description.lower():
				game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_two')
		else:
			game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_two')
			
def artwork_list_create(game_file_name, artwork_base_path):
	for folder in os.listdir(artwork_base_path):
		artwork = get_game_art(game_file_name, os.path.join(artwork_base_path, folder), 'none', 'all')
		if artwork:
			file_types = ['.png', '.jpg', 'ico']
			if any(x in artwork for x in file_types):
				artwork_type = 'image'
			file_types = ['.mp4', '.avi', '.flv']
			if any(x in artwork for x in file_types):
				artwork_type = 'video'
			file_types = ['.pdf']
			if any(x in artwork for x in file_types):
				artwork_type = 'pdf'
			file_types = ['.mp3']
			if any(x in artwork for x in file_types):
				artwork_type = 'audio'
			if artwork_type == 'pdf':
				li = xbmcgui.ListItem(folder, iconImage=os.path.join(addonPath, 'resources', 'media', 'pdf-artwork-icon.png'))
			elif artwork_type == 'audio':
				li = xbmcgui.ListItem(folder, iconImage=os.path.join(addonPath, 'resources', 'media', 'music-artwork-icon.png'))
			else:
				li = xbmcgui.ListItem(folder, iconImage=artwork)
			url = build_url({ 'mode': 'artwork_display', 'artwork': artwork, 'artwork_type': artwork_type })
			if artwork_type in ('video', 'audio'):
				li.setProperty('IsPlayable', 'true')
				url = artwork
				folder = False
			else:
				li.setProperty('IsPlayable', 'false')
				folder = True
			xbmcplugin.addDirectoryItems(addon_handle, [(url, li, folder)])
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

def game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, context_mode):
		game_name = game.find('description').text
		game_file_name = game.attrib['name']
		if game.find('year').text:
			game_year = game.find('year').text
		else:
			game_year =  ''
		if game.find('manufacturer').text:
			game_manufacturer = game.find('manufacturer').text
		else:
			game_manufacturer = ''
		if game.find('rating').text:
			game_rating = game.find('rating').text
		else:
			game_rating = ''
		if game.find('genre').text:
			game_genre = game.find('genre').text
		else:
			game_genre = ''
		game_icon = get_game_art(game_file_name, icon_path, icon_fallback_path, 'image')
		game_fanart = get_game_art(game_file_name, fanart_path, fanart_fallback_path, 'image')
		game_thumb = get_game_art(game_file_name, thumb_path, 'none', 'image')
		game_poster = get_game_art(game_file_name, poster_path, 'none', 'image')
		game_logo = get_game_art(game_file_name, logo_path, 'none', 'image')
		game_clearart = get_game_art(game_file_name, clearart_path, 'none', 'image')
		game_banner = get_game_art(game_file_name, banner_path, 'none', 'image')
		game_media = get_game_art(game_file_name, media_path, 'none', 'image')
		game_trailer = get_game_art(game_file_name, trailer_path, 'none', 'video')
		url = build_url({'mode': 'file', 'foldername': system_name, 'game_name': game_name, 'filename': game_file_name, 'rom_path': rom_path, 'launcher_script': launcher_script, 'rom_extensions': rom_extensions})
		li = xbmcgui.ListItem(game_name, iconImage=game_icon)
		li.setProperty('IsPlayable', 'false')
		li.setArt({ 'thumb': game_thumb, 'fanart': game_fanart, 'poster': game_poster, 'clearlogo': game_logo, 'clearart': game_clearart, 'banner': game_banner, 'discart': game_media })
		li.setInfo( 'video', { 'Title': game_name, 'OriginalTitle': game_file_name, 'Genre': game_genre, 'Year': game_year, 'Director': game_manufacturer, 'Mpaa': game_rating, 'Trailer': game_trailer, 'Plot': system_name, 'Studio': game_manufacturer, 'Path': rom_path, 'launcher_script': launcher_script } )
		contextMenuItems = []
		if context_mode != 'context_two':
			contextMenuItems.append((language(50208), 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'system_name': system_name}) ,))
		if artwork_base_path:
			contextMenuItems.append((language(50209), 'XBMC.Container.Update(%s)' % build_url({'mode': 'artwork', 'game_file_name': game_file_name, 'artwork_base_path': artwork_base_path}) ,))
		contextMenuItems.append((language(50210), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
		contextMenuItems.append((language(50211), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'select_launcher', 'foldername': system_name, 'game_name': game_name, 'filename': game_file_name, 'rom_path': rom_path, 'launcher_script': launcher_script, 'rom_extensions': rom_extensions}) ,))
		li.addContextMenuItems(contextMenuItems)
		xbmcplugin.addDirectoryItems(addon_handle, [(url, li, True)])

if mode is None:
	for system in os.listdir(SYSTEMS_PATH):
		if system.endswith(".xml"):
			system_name = system[:-4]
			system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
			file_check(system_config, system_config)
			tree = ET.parse(system_config)
			root = tree.getroot()
			for item in root.findall('info'):
				if item.find('release_year').text:
					release_year = item.find('release_year').text
				else:
					release_year = ''
				if item.find('manufacturer').text:
					manufacturer = item.find('manufacturer').text
				else:
					manufacturer = ''
				if item.find('description').text:
					description = item.find('description').text
				else:
					description = ''
			system_icon = get_game_art(system_name + '-icon', SYSTEMS_PATH, 'none', 'image')
			system_logo = get_game_art(system_name + '-logo', SYSTEMS_PATH, 'none', 'image')
			system_fanart = get_game_art(system_name + '-fanart', SYSTEMS_PATH, 'none', 'image')
			system_trailer = get_game_art(system_name + '-trailer', SYSTEMS_PATH, 'none', 'video')
			url = build_url({'mode': 'folder', 'foldername': system_name})
			li = xbmcgui.ListItem(system_name, iconImage=system_icon)
			li.setArt({ 'thumb': system_icon, 'fanart': system_fanart, 'clearlogo': system_logo })
			li.setInfo( 'video', { "Title": system_name, "Trailer": system_trailer, 'Year': release_year, 'Director': manufacturer, 'Plot': description } )
			li.setProperty('IsPlayable', 'false')
			contextMenuItems = []
			contextMenuItems.append((language(50201), 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'system_name': 'all'}) ,))
			contextMenuItems.append((language(50202), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
			if system_trailer:
				contextMenuItems.append((language(50203), 'PlayMedia(%s)'  % (system_trailer) ,))
			if system_icon:
				contextMenuItems.append((language(50204), 'ShowPicture(%s)' % (system_icon) ,))
			if system_fanart:
				contextMenuItems.append((language(50205), 'ShowPicture(%s)' % (system_fanart) ,))
			if system_logo:
				contextMenuItems.append((language(50206), 'ShowPicture(%s)'  % (system_logo) ,))
			li.addContextMenuItems(contextMenuItems)
			xbmcplugin.addDirectoryItems(addon_handle, [(url, li, True)])
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'folder':
	system_name = args['foldername'][0]
	system_game_list = args['foldername'][0] + '.xml'
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path = get_system_info(system_config)
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system_game_list))
	root = tree.getroot()
	thread_list = []
	for game in root.findall('game'):
		t = threading.Thread(target=game_list_create, args=(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, icon_fallback_path, fanart_path, fanart_fallback_path, poster_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_one'))
		thread_list.append(t)
	for thread in thread_list:
		thread.start()
	for thread in thread_list:
		thread.join()
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'file':
	emulator_launcher()

elif mode[0] == 'search_input':
	search_string = dialog.input(language(50207), type=xbmcgui.INPUT_ALPHANUM)
	url = build_url({'mode': 'search', 'system_name': ''.join(args.get('system_name')), 'search_string': search_string})
	if len(search_string) == 0:
		if addon.getSetting("BlankSearch") == 'false':
			log(language(50100), language(50101))
			sys.exit()
	xbmc.executebuiltin('Container.Update(%s, refresh)' % url)
	
elif mode[0] == 'search':
	if args.get('search_string'):
		search_string = ''.join(args.get('search_string'))
	else:
		search_string = False
	if ''.join(args.get('system_name')) == 'all':
		thread_list = []
		for system in os.listdir(SYSTEMS_PATH):
			if system.endswith('.xml'):
				t = threading.Thread(target=search, args=(system, search_string))
				thread_list.append(t)
		for thread in thread_list:
			thread.start()
		for thread in thread_list:
			thread.join()
	else:
		system = ''.join(args.get('system_name')) + '.xml'
		search(system, search_string)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
	
elif mode[0] == 'artwork':
	game_file_name = ''.join(args.get('game_file_name'))
	artwork_base_path = ''.join(args.get('artwork_base_path'))
	artwork_list_create(game_file_name, artwork_base_path)

elif mode[0] == 'artwork_display':
	if ''.join(args.get('artwork_type')) == 'image':
		xbmc.executebuiltin('ShowPicture("%s")' % (''.join(args.get('artwork'))))
	if ''.join(args.get('artwork_type')) == 'pdf':
		if not os.path.exists(xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')):
			log_message = 'special://home/addons/plugin.image.pdfreader/resources/lib ' + language(50107)
			log(log_message, language(50108))
			sys.exit()
		addon_pdf = xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')
		sys.path.append(addon_pdf)
		from pdf import pdf
		pdf = pdf()
		pdf.clean_temp()
		pdf.pdf_read(''.join(args.get('artwork')).encode(txt_encode), ''.join(args.get('artwork')).encode(txt_encode), 'true')
		
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

elif mode[0] == 'select_launcher':
	if os.path.exists(LAUNCHER_SCRIPTS):
		select_launcher_list = []
		for alt_launcher in os.listdir(os.path.join(LAUNCHER_SCRIPTS)):
			select_launcher_list.append( alt_launcher, )
		selected_launcher = dialog.select(language(50211), select_launcher_list)
		if selected_launcher == -1:
			sys.exit()
		else:
			selected_launcher = select_launcher_list[selected_launcher]
			if args.get('rom_extensions'):
				rom_extensions = ''.join(args.get('rom_extensions'))
			url = build_url({'mode': 'file', 'foldername': ''.join(args.get('foldername')), 'game_name': ''.join(args.get('game_name')), 'filename': ''.join(args.get('filename')), 'rom_path': ''.join(args.get('rom_path')), 'launcher_script': selected_launcher, 'alt_launcher': 'yes', 'rom_extensions': rom_extensions})			
			xbmc.executebuiltin('RunPlugin(%s)' % url)
	else:
		log_message = language(50109) + LAUNCHER_SCRIPTS
		log(log_message, language(50109))