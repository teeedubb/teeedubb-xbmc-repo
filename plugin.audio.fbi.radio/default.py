import xbmcaddon, xbmcgui, xbmcplugin
import os

addon = xbmcaddon.Addon(id='plugin.audio.fbi.radio')
addonPath = addon.getAddonInfo('path')

addon_handle = int(sys.argv[1])

url = 'http://54.206.93.168:8000/stream'
li = xbmcgui.ListItem('FBi', iconImage=os.path.join(addonPath, 'resources', 'icons', 'fbi.png'))
li.setArt({ 'thumb': os.path.join(addonPath, 'resources', 'icons', 'fbi.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'FBi'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
url = 'http://fbiradio.myradio.click:8000/click'
li = xbmcgui.ListItem('FBi Click', iconImage=os.path.join(addonPath, 'resources', 'icons', 'fbi-click.png'))
li.setArt({ 'thumb': os.path.join(addonPath, 'resources', 'icons', 'fbi-click.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'FBi Click'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
