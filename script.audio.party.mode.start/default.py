import xbmc
import xbmcgui
import xbmcaddon
import time

addon = xbmcaddon.Addon(id='script.audio.party.mode.start')
visTimeout = int(addon.getSetting("visTimeout"))
visInfoHide = addon.getSetting("visInfoHide")
visInfoTimeout = int(addon.getSetting("visInfoTimeout"))

def startPartyMode():
	xbmc.executebuiltin("PlayerControl(Stop)")
	xbmc.executebuiltin("PlayerControl(PartyMode)")
	time.sleep(visTimeout)
	xbmc.executebuiltin("Action(Fullscreen)")
	if visInfoHide == 'true':
		time.sleep(visInfoTimeout)
		xbmc.executebuiltin("Action(Info)")
		
startPartyMode()