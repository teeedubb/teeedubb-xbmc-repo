import xbmcaddon, xbmcgui, xbmcplugin
import os

addon = xbmcaddon.Addon(id='plugin.audio.fbi.radio')
addonPath = addon.getAddonInfo('path')

addon_handle = int(sys.argv[1])

url = 'https://streamer.fbiradio.com/stream'
li = xbmcgui.ListItem('FBi')
li.setArt({ 'icon': os.path.join(addonPath, 'resources', 'icons', 'fbi.png'), 'thumb': os.path.join(addonPath, 'resources', 'icons', 'fbi.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'FBi'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
