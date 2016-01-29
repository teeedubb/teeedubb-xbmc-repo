import xbmcaddon, xbmcgui, xbmcplugin
import os

addon = xbmcaddon.Addon(id='plugin.audio.triple.j')
addonPath = addon.getAddonInfo('path')
addon_handle = int(sys.argv[1])

url = 'http://abcradiolivehls-lh.akamaihd.net/i/triplejnsw_1@327300/index_64_a-b.m3u8?sd=10&rebase=on&hdntl='
li = xbmcgui.ListItem('Triple J Online', iconImage=os.path.join(addonPath, 'resources', 'icons', 'triplej.png'))
li.setArt({ 'thumb': os.path.join(addonPath, 'resources', 'icons', 'triplej.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'Triple J Online'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
url = 'http://abcradiolivehls-lh.akamaihd.net/i/doublejnsw_1@327293/index_64_a-b.m3u8?sd=10&rebase=on&hdntl='
li = xbmcgui.ListItem('Double J Online', iconImage=os.path.join(addonPath, 'resources', 'icons', 'doublej.png'))
li.setArt({ 'thumb': os.path.join(addonPath, 'resources', 'icons', 'doublej.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'Double J Online'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
url = 'http://abcradiolivehls-lh.akamaihd.net/i/triplejunearthed_1@327301/index_64_a-p.m3u8?sd=10&rebase=on&hdntl='
li = xbmcgui.ListItem('Triple J Uneartherd Online', iconImage=os.path.join(addonPath, 'resources', 'icons', 'unearthed.png'))
li.setArt({ 'thumb': os.path.join(addonPath, 'resources', 'icons', 'unearthed.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'Triple J Uneartherd Online'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)


#xbmc.executebuiltin("PlayMedia(http://www.abc.net.au/res/streaming/audio/aac/triplej.pls)")