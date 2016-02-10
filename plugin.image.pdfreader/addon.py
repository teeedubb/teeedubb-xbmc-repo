#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
How to use PDF Reader - Add these lines to your py

try:
	addon_pdf = xbmc.translatePath('special://home/addons/plugin.image.pdfreader/resources/lib')
	sys.path.append(addon_pdf)
	from pdf import pdf		# For pdf
	pdf = pdf()				# For pdf
	from pdf import cbx		# For cbr and cbz
	cbx = cbx()				# For cbr and cbz
except:
	dialog = xbmcgui.Dialog()
	dialog.ok("Erro!","Não foi encontrado o add-on PDF Reader.","Por favor, instale-o.")
	xbmc.executebuiltin('XBMC.ActivateWindow(Home)')
	
###################################

#PDF Functions:

#open_settings():			# Open addon settings
#pdf_read(name,url,videoaddon):		# Read and play pdf - url = url or filepath - videoaddon = (bool) optional
#pdf_type(filepath):		# Returns the type of PDF
#pdf_name(filepath):		# Returns the name of PDF
#clean_temp():				# Delete temporary files

#You must include 'pdf.' before functions you want to use. Example: pdf.pdf_read(name,url)

####################################

#CBX Functions:

#cbx_read(name,url,videoaddon):		# Read and play cbr/cbz - url = url or filepath - videoaddon = (bool) optional
#clean_temp():				# Delete temporary files

#You must include 'cbx.' before functions you want to use. Example: cbx.cbx_read(name,url)
"""

##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,random
from resources.lib.pdf import pdf
from resources.lib.pdf import cbx
pdf = pdf()
cbx = cbx()

h = HTMLParser.HTMLParser()

versao = '1.0.2'

addon_id = 'plugin.image.pdfreader'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
traducaoma = selfAddon.getLocalizedString

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

################################################## 

#MENUS############################################

def CATEGORIES():
	pdf._mensagem_inicial()
	cbx.clean_temp()
	addDir(traducao(2000),'-',4,artfolder + 'open.png',False)
	addDir(traducao(2008),'-',6,artfolder + 'opencbx.png',False)
	addLink('','','-')
	addDir('[B][COLOR white]'+traducao(2001)+'[/COLOR][/B]','-',3,artfolder + 'settings.png',False)
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]'+traducao(2004)+' (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel==traducao(2005): addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]'+traducao(2006)+' ('+ disponivel + '). '+traducao(2007)+'[/COLOR][/B]','',artfolder + 'versao.png')
	xbmc.executebuiltin("Container.SetViewMode(50)")

###################################################################################
#FUNCOES
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.image.pdfreader/addon.xml')
		match=re.compile('<addon id="plugin.image.pdfreader" name="PDF Reader" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match=traducao(2005)
	return match

def abrir_CBX():
	dialog = xbmcgui.Dialog()
	file = dialog.browse(1,traducao(2008),"myprograms")
	if file == '': return
	if '.cbr' not in file and '.cbx' not in file:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(2002),traducao(2009))
		return
	cbx.cbx_read('CBX',file)
	
def abrir_PDF():
	dialog = xbmcgui.Dialog()
	file = dialog.browse(1,traducao(2000),"myprograms")
	if file == '': return
	if '.pdf' not in file and '.PDF' not in file:
		dialog = xbmcgui.Dialog()
		dialog.ok(traducao(2002),traducao(2003))
		return
	pdf.pdf_read('PDF_'+pdf.pdf_name(file),file)
	
###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', artfolder + 'black-background.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', artfolder + 'black-background.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]						
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: pdf._play(name,url) # NAO APAGAR
elif mode==2: pdf.pdf_read(name,url)
elif mode==3: selfAddon.openSettings()
elif mode==4: abrir_PDF()
elif mode==5: cbx._play(name,url) # NAO APAGAR
elif mode==6: abrir_CBX()
elif mode==100: cbx.cbx_read(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))