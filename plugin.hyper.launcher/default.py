# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import izip
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
import shutil
import threading
import xml.etree.ElementTree as ET

#set text encoding.... ugh...
try:
	txt_encode = sys.getfilesystemencoding()
except:
	txt_encode = 'utf-8'
reload(sys)  
sys.setdefaultencoding('utf-8')

#variables
scriptid = 'plugin.hyper.launcher'
addon = xbmcaddon.Addon(id='plugin.hyper.launcher')
addonPath = addon.getAddonInfo('path')
addonDataPath = xbmc.translatePath('special://profile/addon_data/%s' % scriptid)
addonIcon = addon.getAddonInfo('icon')
addonVersion = addon.getAddonInfo('version')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
suspendAudio = addon.getSetting("SuspendAudio")
backgroundKodi = addon.getSetting("BackgroundKodi")
searchThreading = addon.getSetting("SearchThreading")
defaultSearchView = int(addon.getSetting("DefaultSearchView"))
defaultImageView = int(addon.getSetting("DefaultImageView"))
ghostscriptDpi = int(addon.getSetting("GhostscriptDpi"))
ghostscriptDSF = int(addon.getSetting("GhostscriptDSF"))
ghostscriptPath = addon.getSetting("GhostscriptPath")
ghostscriptUse = addon.getSetting("GhostscriptUse")
pluginPdfReaderUse = addon.getSetting("PluginPdfReaderUse")
extPdfReaderPath = addon.getSetting("ExtPdfReaderPath")
extPdfReaderUse = addon.getSetting("ExtPdfReaderUse")
showAllGames = addon.getSetting("ShowAllGames")
createSystemArtworkFolder = addon.getSetting("CreateSystemArtworkFolder")
additionalLogging = addon.getSetting("AdditionalLogging")

#addon paths
SYSTEMS_PATH = os.path.join(addonDataPath, 'systems')
SYSTEMS_CONFIG_PATH = os.path.join(addonDataPath, 'systems_config')
SYSTEMS_ARTWORK_PATH = os.path.join(addonDataPath, 'systems_artwork')
LAUNCHER_SCRIPTS = os.path.join(addonDataPath, 'launcher_scripts')
RESTART_FILE = os.path.join(addonDataPath, 'restart_file.txt')
SUPRESS_VIDEO_FILE = os.path.join(addonDataPath, 'suppress_video_file.txt')

#stop video playback when launched
if xbmc.Player().isPlayingVideo():
	xbmc.Player().stop()

#create addon paths
if not os.path.exists(addonDataPath): 
	os.makedirs(addonDataPath)
if not os.path.exists(SYSTEMS_PATH): 
	os.makedirs(SYSTEMS_PATH)
if not os.path.exists(SYSTEMS_ARTWORK_PATH): 
	os.makedirs(SYSTEMS_ARTWORK_PATH)
if not os.path.exists(SYSTEMS_CONFIG_PATH): 
	os.makedirs(SYSTEMS_CONFIG_PATH)
if not os.path.exists(LAUNCHER_SCRIPTS): 
	os.makedirs(LAUNCHER_SCRIPTS)

#addon 
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)

#sort methods
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

def vlog(msg):
	if additionalLogging == 'true':
		xbmc.log('%s: %s' % (scriptid + '.verbose.log', msg))

def prevent_video_playback(option):
	if option == 'start':
		if not os.path.exists(SUPRESS_VIDEO_FILE):
			try:
				f = open(SUPRESS_VIDEO_FILE, 'w')
				f.write('prevent_video_playback')
				f.close()
			except:
				pass
	elif option == 'stop':
		if os.path.exists(SUPRESS_VIDEO_FILE):
			try:
				xbmc.sleep(2000)
				os.remove(SUPRESS_VIDEO_FILE)
			except:
				pass

def file_check(file, required_file):
	if not file:
		file = required_file
	if not os.path.isfile(file):
		log_message = language(50102) + ': "%s"' % file
		log(log_message, log_message)
		sys.exit()
		
def get_game_art(game_file_name, path, fallback_path, type):
	fanart = 'false'
	if type == 'video':
		fanart_file_types = ('.mp4', '.avi', '.flv')
	elif type == 'image':
		fanart_file_types = ('.png', '.jpg', '.ico')
	else:
		fanart_file_types = ('.png', '.jpg', '.mp4', '.mp3', '.pdf', '.ico', '.flv', '.avi')
	for fanart_file_type in fanart_file_types:
		artwork = os.path.join(path, game_file_name + fanart_file_type)
		if os.path.isfile(artwork):
			fanart = artwork
		if fanart != 'false':
			vlog('Found artwork, breaking')
			break
	vlog('Artwork:')
	vlog(fanart)
	return fanart
	
def get_system_info(system_config):
	tree = ET.parse(system_config)
	root = tree.getroot()
	input1 = ['rom_path', 'rom_extensions', 'launcher_script']
	d1 = {}
	for item in root.findall('config'):
		for i1 in input1:
			if item.find(i1).text:
				d1[i1] = item.find(i1).text
				log_message = 'Found config: "%s" for "%s"' % (system_config, i1)
				log(log_message, False)
			else:
				if i1 != 'rom_extensions':
					log_message = 'Required config parameter missing: %s, %s' % (system_config, i1)
					log(log_message, language(50105))
				else:
					d1[i1] = 'false'
	input2 = ['base_path', 'icon', 'poster', 'poster_fallback', 'fanart', 'fanart_fallback', 'thumb', 'logo', 'clearart', 'banner', 'media', 'trailer']
	output2 = ['artwork_base_path', 'icon_path', 'poster_path', 'poster_fallback_path', 'fanart_path', 'fanart_fallback_path', 'thumb_path', 'logo_path', 'clearart_path', 'banner_path', 'media_path', 'trailer_path']
	for item in root.findall('artwork'):
		for i2,o2 in izip(input2, output2):
			log('yoyoyoyoyo', False)
			log(item.find(i2), False)
			if item.find(i2) != None and item.find(i2).text != None and os.path.exists(item.find(i2).text):
				log('Path exists:', False)
				log(item.find(i2).text, False)
				d1[o2] = item.find(i2).text
			else:
				d1[o2] = 'false'
	return (d1['rom_path'], d1['rom_extensions'], d1['launcher_script'], d1['artwork_base_path'], d1['icon_path'], d1['poster_path'], d1['poster_fallback_path'], d1['fanart_path'], d1['fanart_fallback_path'], d1['thumb_path'], d1['logo_path'], d1['clearart_path'], d1['banner_path'], d1['media_path'], d1['trailer_path'])
	
def emulator_launcher():
	prevent_video_playback('start')
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
						log_message = 'Directory does not exist: ' + os.path.join(rom_path, selected_game)
						log(log_message, language(50109))
		if not args.get('alt_launcher'):
			for item in root.findall('alt_launchers'):
				for game in item.iter('game'):
					if selected_game in game.attrib['name']:
						launcher_script = game.find('launcher').text
		if args.get('rom_extensions') == ['false']:
			search_item = os.path.join(rom_path, selected_game + '.*')
			rom_full_path_list = glob.glob('%s' % search_item)
			rom_full_path = ''.join(rom_full_path_list[0])
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
			log('Attempted command is:', False)
			log(cmd, False)
			if suspendAudio == 'true':
				xbmc.audioSuspend()
				log('Suspending Kodi audio', False)
			if backgroundKodi == 'true':
				proc_h = subprocess.Popen(cmd.encode(txt_encode), shell=True, close_fds=False)
				while proc_h.returncode is None:
					xbmc.sleep(500)
					proc_h.poll()
				del proc_h		
			else:
				subprocess.Popen(cmd.encode(txt_encode), shell=True, close_fds=True)
			prevent_video_playback('stop')
			xbmc.audioResume()
	else:
		log('No selected game', language(50110))

def search(system, search_string):
	system_name = system[:-4]
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	file_check(system_config, system_config)
	log_message = 'Reading: %s' % system_config
	log(log_message, False)
	rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, poster_path, poster_fallback_path, fanart_path, fanart_fallback_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path = get_system_info(system_config)
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system))
	root = tree.getroot()
	for game in root.findall('game'):
		game_description = game.find('description').text
		if search_string != False:
			if search_string.lower() in game_description.lower():
				game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, poster_path, poster_fallback_path, fanart_path, fanart_fallback_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_two')
		else:
			game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, poster_path, poster_fallback_path, fanart_path, fanart_fallback_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_two')

def artwork_list_find(artwork, folder, game_file_name):
	artwork_type = 'false'
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
	if artwork_type != 'false':
		if artwork_type == 'pdf':
			li = xbmcgui.ListItem(folder, iconImage=os.path.join(addonPath, 'resources', 'media', 'pdf-artwork-icon.png'))
		elif artwork_type == 'audio':
			li = xbmcgui.ListItem(folder, iconImage=os.path.join(addonPath, 'resources', 'media', 'music-artwork-icon.png'))
		else:
			li = xbmcgui.ListItem(folder, iconImage=artwork)
		artworkname = game_file_name + '.' + folder
		url = build_url({ 'mode': 'artwork_display', 'artwork': artwork, 'artwork_type': artwork_type, 'game_name': artworkname})
		if artwork_type in ('video', 'audio'):
			li.setProperty('IsPlayable', 'true')
			url = artwork
			isfolder = False
		elif artwork_type in ('pdf'):
			isfolder = False
		else:
			li.setProperty('IsPlayable', 'false')
			isfolder = True
		xbmcplugin.addDirectoryItems(addon_handle, [(url, li, isfolder)])

def artwork_list_create(game_file_name, artwork_base_path, game_name):
	prevent_video_playback('start')
	if (('plugin.hyper.launcher' in artwork_base_path and 'systems_artwork' in artwork_base_path and '.xml' in game_file_name)):
		for file in os.listdir(artwork_base_path):
			artwork = get_game_art(file[:-4], artwork_base_path, 'none', 'all')	
			if artwork:
				artwork_list_find(artwork, file[:-4], game_file_name)
	else:
		for folder in os.listdir(artwork_base_path):
			artwork = get_game_art(game_file_name, os.path.join(artwork_base_path, folder), 'none', 'all')
			if artwork:
				artwork_list_find(artwork, folder, game_file_name)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
	prevent_video_playback('stop')

def game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, poster_path, poster_fallback_path, fanart_path, fanart_fallback_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, context_mode):
	if game.find('enabled') != None and game.find('enabled').text != 'Yes':
		return
	game_name = game.find('description').text
	game_file_name = game.attrib['name']
	li = xbmcgui.ListItem('%s' % game_name)
	input1 = ['year', 'dev', 'manufacturer', 'rating', 'genre', 'score', 'story', 'player']
	label1 = ['Year', 'Studio', 'Director', 'Mpaa', 'Genre', 'Rating', 'Plot', 'Writer']
	d1 = {}
	for i1,l1 in izip(input1, label1):
		if game.find(i1) != None and game.find(i1).text:
			d1[l1] = game.find(i1).text
	input2 = [icon_path, fanart_fallback_path, fanart_path, thumb_path, poster_fallback_path, poster_path, logo_path, clearart_path, banner_path, media_path, trailer_path]
	label2 = ['icon', 'fanart', 'fanart', 'thumb', 'poster', 'poster', 'clearlogo', 'clearart', 'banner', 'discart', 'trailer']
	d2 = {}
	for i2, l2 in izip(input2, label2):
		f2 = 'false'
		if i2 != 'false':
			vlog('Path exists, checking for art')
			if i2 and l2 == 'trailer':
				f2 = get_game_art(game_file_name, i2, 'none', 'video')
			else:
				f2 = get_game_art(game_file_name, i2, 'none', 'image')
		else:
			vlog('Path does not exist for artwork type:')
		if f2 != 'false':
			if i2 and l2 == 'trailer':
				d1[l2] = f2
			else:
				d2[l2] = f2
	d1.update({ 'Title': game_name, 'OriginalTitle': game_file_name, 'launcher_script': launcher_script })
	li.setArt(d2)
	b_url = build_url({'mode': 'artwork', 'game_name': game_name, 'game_file_name': game_file_name, 'artwork_base_path': artwork_base_path})
	d1['Album'] = b_url
	li.setInfo('video', d1)			
	url = build_url({'mode': 'file', 'foldername': system_name, 'game_name': game_name, 'filename': game_file_name, 'rom_path': rom_path, 'launcher_script': launcher_script, 'rom_extensions': rom_extensions})
	li.setProperty('IsPlayable', 'false')
	contextMenuItems = []
	if context_mode != 'context_two':
		contextMenuItems.append((language(50208), 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'foldername': 'none', 'system_name': system_name}) ,))
	if artwork_base_path:
		contextMenuItems.append((language(50209), 'XBMC.Container.Update(%s)' % b_url ,))
	contextMenuItems.append((language(50210), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
	contextMenuItems.append((language(50211), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'select_launcher', 'foldername': system_name, 'game_name': game_name, 'filename': game_file_name, 'rom_path': rom_path, 'launcher_script': launcher_script, 'rom_extensions': rom_extensions}) ,))
	li.addContextMenuItems(contextMenuItems)	
	listing.append((url, li, True))
prevent_video_playback('stop')

def create_system_artwork_folder():
	if not os.path.exists(system_artwork_path):
		os.makedirs(system_artwork_path)
		for file in os.listdir(SYSTEMS_PATH):
			if system_name+'-' in file:
				if not os.path.exists(os.path.join(system_artwork_path, file)):
					shutil.move(os.path.join(SYSTEMS_PATH, file), os.path.join(system_artwork_path, file))
		log_message = 'Creating system artwork directory %s and moving files' % system_artwork_path
		log(log_message, False)
	addon.setSetting(id="CreateSystemArtworkFolder", value="false")

if mode is None:
	showAllGamesTrailers = []
	listing = []
	for system in os.listdir(SYSTEMS_PATH):
		if system.endswith(".xml"):
			system_name = system[:-4]
			system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
			system_artwork_path = os.path.join(SYSTEMS_ARTWORK_PATH, system_name)
			if createSystemArtworkFolder == 'true':
				create_system_artwork_folder()
			file_check(system_config, system_config)
			tree = ET.parse(system_config)
			root = tree.getroot()
			input1 = ['release_year', 'manufacturer', 'manufacturer', 'description']
			label1 = ['Year', 'Studio', 'Director', 'Plot']
			d1 = {}
			for item in root.findall('info'):
				for i1,l1 in izip(input1, label1):
					if item.find(i1).text:
						d1[l1] = item.find(i1).text
			d2 = {}
			system_art = ['icon', 'poster', 'logo', 'fanart', 'trailer']
			system_art_out = ['icon', 'poster', 'clearlogo', 'fanart', 'trailer']
			system_art_type = ['image', 'image', 'image', 'image', 'video' ]
			for sa, sao, sat in izip(system_art, system_art_out, system_art_type):
				game_art = get_game_art(system_name + '-' + sa, system_artwork_path, 'none', sat)
				if sa == 'trailer' and sao == 'trailer':
					d1[sao] = game_art
				else:
					d2[sao] = game_art
			li = xbmcgui.ListItem(system_name) #, iconImage=d2['icon'])
			d1.update({ "Title": system_name })
			li.setArt(d2)
			li.setInfo('video', d1)			
			if showAllGames == 'true' and d1['trailer']:
				showAllGamesTrailers.append((d1['trailer'] , ))
			url = build_url({'mode': 'folder', 'foldername': system_name})
			li.setProperty('IsPlayable', 'false')
			contextMenuItems = []
			contextMenuItems.append((language(50201), 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'foldername': 'none', 'system_name': 'all'}) ,))
			contextMenuItems.append((language(50202), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
			if os.path.exists(system_artwork_path):
				contextMenuItems.append((language(50209), 'XBMC.Container.Update(%s)' % build_url({'mode': 'artwork', 'game_name': system_name, 'game_file_name': system, 'artwork_base_path': system_artwork_path}) ,))
			li.addContextMenuItems(contextMenuItems)
			listing.append((url, li, True))
	if showAllGames == 'true':
		log('Show all games enabled', False)
		if showAllGamesTrailers:
			system_trailer = random.choice(showAllGamesTrailers)
			log('All games system trailer:', False)
			log(system_trailer, False)
		else:
			system_trailer = 'false'
			log('No trailers to choose from for all games item', False)
		li = xbmcgui.ListItem('All Games', iconImage=os.path.join(addonPath, 'resources', 'media', 'all-games-icon.png'))
		li.setArt({ 'thumb': os.path.join(addonPath, 'resources', 'media', 'all-games-icon.jpg'), 'fanart': os.path.join(addonPath, 'fanart.jpg'), 'clearlogo': os.path.join(addonPath, 'resources', 'media', 'all-games-logo.png'), 'poster': os.path.join(addonPath, 'resources', 'media', 'all-games-poster.jpg') })
		li.setInfo( 'video', { 'Title': 'All Games', 'Trailer': ''.join(system_trailer), 'Year': 'All', 'Director': 'All' } )
		url = build_url({'mode': 'search_input', 'foldername': 'all_games_list', 'system_name': 'all'})
		contextMenuItems = []
		contextMenuItems.append((language(50201), 'XBMC.Container.Update(%s)' % build_url({'mode': 'search_input', 'foldername': 'none', 'system_name': 'all'}) ,))
		contextMenuItems.append((language(50202), 'XBMC.RunPlugin(%s)' % build_url({'mode': 'random_focus'}) ,))
		li.addContextMenuItems(contextMenuItems)		
		listing.append((url, li, True))
	xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)

elif mode[0] == 'folder':
	prevent_video_playback('start')
	system_name = args['foldername'][0]
	system_game_list = args['foldername'][0] + '.xml'
	system_config = os.path.join(SYSTEMS_CONFIG_PATH, system_name + '-config.xml')
	rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, poster_path, poster_fallback_path, fanart_path, fanart_fallback_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path = get_system_info(system_config)
	tree = ET.parse(os.path.join(SYSTEMS_PATH, system_game_list))
	root = tree.getroot()
	listing = []
	for game in root.findall('game'):
		game_list_create(game, system_name, rom_path, rom_extensions, launcher_script, artwork_base_path, icon_path, poster_path, poster_fallback_path, fanart_path, fanart_fallback_path, thumb_path, logo_path, clearart_path, banner_path, media_path, trailer_path, 'context_one')
	xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
	prevent_video_playback('stop')
	log('Folder loaded:', False)
	log(system_game_list, False)

elif mode[0] == 'file':
	emulator_launcher()

elif mode[0] == 'search_input':
	prevent_video_playback('start')
	listing = []
	search_string = False
	all_games_list = ''.join(args.get('foldername'))
	all_systems = ''.join(args.get('system_name'))
	if not all_games_list == 'all_games_list':
		search_string = dialog.input(language(50207), type=xbmcgui.INPUT_ALPHANUM)
		if len(search_string) == 0:
			log('Blank search, exiting', False)
			sys.exit()
	if any ((all_systems == 'all', all_games_list == 'all_games_list')):
		if searchThreading == 'true':
			log('Using threading for all systems search', False)
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
			log('Not using threading for all systems search', False)
			for system in os.listdir(SYSTEMS_PATH):
				if system.endswith('.xml'):
					search(system, search_string)
	else:
		log('Single system search', False)
		system = ''.join(args.get('system_name')) + '.xml'
		search(system, search_string)
	xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))

	xbmc.executebuiltin("Container.SetViewMode(%s)" % defaultSearchView)
	xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
	prevent_video_playback('stop')
	
elif mode[0] == 'artwork':
	artwork_list_create(''.join(args.get('game_file_name')), ''.join(args.get('artwork_base_path')), ''.join(args.get('game_name')))

elif mode[0] == 'artwork_display':
	artwork = ''.join(args.get('artwork'))
	game_name = ''.join(args.get('game_name'))
	if ''.join(args.get('artwork_type')) == 'pdf':
		xbmc.executebuiltin("ActivateWindow(busydialog)")
		if ghostscriptUse == 'true' and os.path.isfile(ghostscriptPath):
			if os.path.exists(xbmc.translatePath('special://temp/%s' % scriptid)):
				log('Temp PDF dir exists, deleteing', False)
				shutil.rmtree(xbmc.translatePath('special://temp/%s' % scriptid))
			temp_directory = xbmc.translatePath('special://temp/%s/%s' % (scriptid, ''.join(args.get('game_name'))))
			log_message = 'Temp directory: %s' % temp_directory
			log(log_message, False)
			os.makedirs(temp_directory)
			output_file = '%s/%%03d.png' % (temp_directory)
			cmd = '"%s" -sDEVICE=png16m -dDownScaleFactor=%s -dNumRenderingThreads=4 -dSAFER -dBATCH -dNOPAUSE -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -r%s -o "%s" "%s"' % (ghostscriptPath, ghostscriptDSF, ghostscriptDpi, output_file, ''.join(args.get('artwork')))
			log_message = 'Ghostscript command: %s' % cmd
			log(log_message, False)
			proc_h = subprocess.Popen(cmd.encode(txt_encode), shell=True, close_fds=False)
			while proc_h.returncode is None:
				xbmc.sleep(50)
				proc_h.poll()
			del proc_h
			xbmc.executebuiltin('ActivateWindow(Pictures,"%s",return)' %  temp_directory)
			xbmc.executebuiltin('Container.SetViewMode(%s)' % defaultImageView)
		elif os.path.exists(xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')) and pluginPdfReaderUse == 'true':
			addon_pdf = xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')
			sys.path.append(addon_pdf)
			from pdf import pdf
			pdf = pdf()
			pdf.clean_temp()
			log('Using plugin.image.pdfreader', False)
			pdf.pdf_read(''.join(args.get('artwork')).encode(txt_encode), ''.join(args.get('artwork')).encode(txt_encode), 'true')
		elif extPdfReaderUse == 'true' and os.path.isfile(extPdfReaderPath):
			cmd = '"%s" "%s"' %  (extPdfReaderPath, ''.join(args.get('artwork')))
			proc_h = subprocess.Popen(cmd.encode(txt_encode), shell=True, close_fds=False)
			while proc_h.returncode is None:
				xbmc.sleep(50)
				proc_h.poll()
			del proc_h
		else:
			log('Additional software required to view PDFs', language(50107))
		xbmc.executebuiltin( "Dialog.Close(busydialog)" ) 
	elif ''.join(args.get('artwork_type')) == 'image':
		xbmc.executebuiltin('ShowPicture("%s")' % (''.join(args.get('artwork'))))
	xbmc.executebuiltin("Dialog.Close(busydialog)")
		
elif mode[0] == 'random_focus':
	total_list_items = int(xbmc.getInfoLabel('Container(id).NumItems'))
	current_selection = int(xbmc.getInfoLabel('Container(id).CurrentItem'))
	win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	cid = win.getFocusId()
	random_pool = range(1, current_selection) + range(current_selection + 1, total_list_items + 1)
	if len(random_pool) > 0:
		random_listi = random.choice(random_pool)
		random_list_item = (random_listi - current_selection)
		xbmc.executebuiltin('Control.Move(%s, %s)' % (cid, random_list_item))

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
				url = build_url({'mode': 'file', 'foldername': ''.join(args.get('foldername')), 'game_name': ''.join(args.get('game_name')), 'filename': ''.join(args.get('filename')), 'rom_path': ''.join(args.get('rom_path')), 'launcher_script': selected_launcher, 'alt_launcher': 'yes', 'rom_extensions': ''.join(args.get('rom_extensions'))})	
			else:
				url = build_url({'mode': 'file', 'foldername': ''.join(args.get('foldername')), 'game_name': ''.join(args.get('game_name')), 'filename': ''.join(args.get('filename')), 'rom_path': ''.join(args.get('rom_path')), 'launcher_script': selected_launcher, 'alt_launcher': 'yes'})
			xbmc.executebuiltin('RunPlugin(%s)' % url)
	else:
		log_message = 'Directory does not exist: ' + LAUNCHER_SCRIPTS
		log(log_message, language(50109))

elif mode[0] == 'hls_settings':
	if os.path.exists(xbmc.translatePath('special://home/addons/service.hyper.launcher')):
		xbmc.executebuiltin('Addon.OpenSettings(service.hyper.launcher)')
	else:
		log('service.hyper.launcher not installed', language(50203))
