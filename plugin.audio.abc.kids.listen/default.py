import xbmcaddon, xbmcgui, xbmcplugin
import os

addon = xbmcaddon.Addon(id='plugin.audio.abc.kids.listen')
addonPath = addon.getAddonInfo('path')

addon_handle = int(sys.argv[1])

url = 'http://live-radio01.mediahubaustralia.com/XTDW/aac/'
li = xbmcgui.ListItem('ABC KIDS Listen AAC+')
#ABC KIDS Listen AAC+', iconImage=os.path.join(addonPath, 'icon.png'))

li.setArt({ 'icon': os.path.join(addonPath, 'icon.png'), 'thumb': os.path.join(addonPath, 'icon.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'ABC KIDS Listen AAC+'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
url = 'http://live-radio01.mediahubaustralia.com/XTDW/mp3/'
li = xbmcgui.ListItem('ABC KIDS Listen MP3')
#ABC KIDS Listen MP3', iconImage=os.path.join(addonPath, 'icon.png'))
li.setArt({ 'icon': os.path.join(addonPath, 'icon.png'), 'thumb': os.path.join(addonPath, 'icon.png'), 'fanart': os.path.join(addonPath, 'fanart.jpg') })
li.setInfo( 'music', { "Title": 'ABC KIDS Listen MP3'})
li.setProperty('IsPlayable', 'True')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
