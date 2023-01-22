import xbmcaddon, xbmcgui, xbmcplugin
import os

addon = xbmcaddon.Addon(id='plugin.audio.triple.j')
addonPath = addon.getAddonInfo('path')
addon_handle = int(sys.argv[1])

url = 'https://mediaserviceslive.akamaized.net/hls/live/2038308/triplejnsw/index.m3u8'
li = xbmcgui.ListItem('Triple J Online')
li.setArt({ 'icon': os.path.join(addonPath, 'resources', 'icons', 'triplej.png'), 'thumb': os.path.join(addonPath, 'resources', 'icons', 'triplej.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'Triple J Online'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
url = 'https://mediaserviceslive.akamaized.net/hls/live/2038315/doublejnsw/index.m3u8'
li = xbmcgui.ListItem('Double J Online')
li.setArt({ 'icon': os.path.join(addonPath, 'resources', 'icons', 'doublej.png'), 'thumb': os.path.join(addonPath, 'resources', 'icons', 'doublej.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'Double J Online'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
url = 'https://mediaserviceslive.akamaized.net/hls/live/2038305/triplejunearthed/index.m3u8'
li = xbmcgui.ListItem('Triple J Uneartherd Online')
li.setArt({ 'icon': os.path.join(addonPath, 'resources', 'icons', 'unearthed.png'), 'thumb': os.path.join(addonPath, 'resources', 'icons', 'unearthed.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'Triple J Uneartherd Online'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)


#xbmc.executebuiltin("PlayMedia(http://www.abc.net.au/res/streaming/audio/aac/triplej.pls)")
