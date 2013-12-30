import xbmc
import xbmcgui
import xbmcaddon
import time

xbmc.executebuiltin("XBMC.PlayerControl(Stop)")
xbmc.executebuiltin("XBMC.PlayerControl(PartyMode)")
time.sleep(5)
xbmc.executebuiltin("XBMC.Action(Fullscreen)")

