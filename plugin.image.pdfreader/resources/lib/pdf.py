#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous

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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,random

h = HTMLParser.HTMLParser()

addon_id = 'plugin.image.pdfreader'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
temp = addonfolder + '/resources/temp/'
thumbs = selfAddon.getSetting('thumbs')
thumbs2 = selfAddon.getSetting('thumbs2')
local = selfAddon.getSetting('local')
local_folder = selfAddon.getSetting('local-folder')
traducaoma= selfAddon.getLocalizedString

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

class pdf:
	def _mensagem_inicial(self):
		if selfAddon.getSetting("mensagem") == "true":
			dialog = xbmcgui.Dialog()
			dialog.ok(traducao(3000),traducao(3001),traducao(3002),traducao(3003))
			dialog.ok(traducao(3000),traducao(3004))
			selfAddon.setSetting('mensagem',value='false')
		
	def open_settings(self):		#Open addon settings
		selfAddon.openSettings()

	def pdf_read(self,name,url,videoaddon=False):	# Read and play pdf
		if videoaddon: 
			xbmc.executebuiltin("ActivateWindow(busydialog)")
			xbmc.executebuiltin('XBMC.RunAddon(plugin.image.pdfreader)')
			xbmc.sleep(2000)
			xbmc.executebuiltin("Dialog.Close(busydialog)")
		name = re.sub('[^a-z A-Z0-9\n\.]', '', name)
		self._mensagem_inicial()
		self.clean_temp()
		if os.path.isfile(url) is True: pdf_path=url
		else:
			if local != 'false':
				pdf_path = self._download_local(url,name)
				if pdf_path == '-': return
			else:
				if not self._download(url): return
				pdf_path = os.path.join(temp,'temp.pdf')
		xbmc.executebuiltin('XBMC.Container.Update(%s?mode=1&url=%s&name=%s)' % ('plugin://plugin.image.pdfreader/', urllib.quote_plus(pdf_path),name))

	def _play(self,name,url):
		images_name=[]
		try:
			f = open(temp+'names.txt',"r")
			aux = f.readlines()
			f.close()
			for a in aux:
				images_name.append(a.replace('\n',''))
		except:
			name = name.replace('/', '').replace('\\', '').replace(':', '').replace('*', '')
			name = name.replace('"', '').replace('?', '').replace('>', '').replace('<', '').replace('|', '')
			type = self.pdf_type(url)
			if not os.path.isfile(url): return
			images_name = self._pdf_image(name,url,type)
		if not images_name: 
			dialog = xbmcgui.Dialog()
			dialog.ok(traducao(3005),traducao(3006))
			return
		i=1
		for image_name in images_name:
			image_path = os.path.join(temp,image_name)
			if thumbs == 'false': self._addPage(traducao(3007)+str(i),image_path,artfolder+str(i)+'.png')
			else: self._addPage(traducao(3007)+str(i),image_path,image_path)
			i += 1
		xbmc.executebuiltin("Container.SetViewMode(500)")
		
	def pdf_type(self,ficheiro):	#Returns the type of PDF
		pdf = file(ficheiro, "rb").read()
		if re.search("\xff\xd8",pdf) and re.search("\xff\xd9",pdf): return 'jpg'
		elif re.search("\x89\x50\x4E\x47",pdf) and re.search("\xAE\x42\x60\x82",pdf): return 'png'
		else: return '-'
		
	def pdf_name(self,path):	#Returns the name of PDF
		i=0
		index = 0
		while i != -1:
			i = path.find("\\", index)
			if i != -1: index = i + 1
		return path[index:].replace('.pdf','').replace('.PDF','')
		
	def _pdf_image(self,name,ficheiro,type,save_path=temp):
		if type == 'jpg':
			startmark="\xff\xd8"
			endmark="\xff\xd9"
			endfix = 2
		elif type == 'png':
			startmark="\x89\x50\x4E\x47"
			endmark="\xAE\x42\x60\x82"
			endfix = 4
		else: return 0
		pdf = file(ficheiro, "rb").read()
		startfix = 0
		i = 0
		dim = 0
		images_name = []
		while True:
			istream = pdf.find("stream", i)
			if istream < 0:
				break
			istart = pdf.find(startmark, istream, istream+20) #str.find(sub[, start[, end]])
			if istart < 0:
				i = istream+20 #20 bytes - cada letra precisa de 1 byte
				continue
			iendstream = pdf.find("endstream", istart)
			if iendstream < 0:
				raise Exception("Não encontrou o fim de stream!")
			iend = pdf.find(endmark, iendstream-20)
			if iend < 0:
				raise Exception("Não encontrou o fim da Imagem!")
			 
			istart += startfix
			iend += endfix

			image = pdf[istart:iend]
			if thumbs == 'false': aux = name+'_'+str(dim)+'.'+type
			else:
				if thumbs2 == '0': aux = name+'-'+str(dim)+'.'+type
				else: aux = name+'_'+str(dim)+'_%d=%d' % (random.randint(1, 10000), random.randint(1, 10000)) + '.'+type
			if sys.getsizeof(image) > 10000 or selfAddon.getSetting('limite')=='false':
				image_path = os.path.join(save_path,aux)
				imagefile = file(image_path, "wb")
				imagefile.write(image)
				imagefile.close()
				images_name.append(aux)
				dim += 1
			i = iend
		f = open(temp+'names.txt',"w")
		for image_name in images_name:
			f.write(image_name+'\n')
		f.close()
		return images_name

	def clean_temp(self):	#Delete temporary files
		for f in os.listdir(temp):
			file_path = os.path.join(temp, f)
			while os.path.exists(file_path): 
				try: os.remove(file_path); break 
				except: pass

	def _addPage(self,name,url,iconimage):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultImage.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', artfolder + 'black-background.jpg')
		liz.setInfo( type='image', infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		return ok
				
	#Download PDF
	def _download_local(self,url,name):
		if local_folder == '':
			dialog = xbmcgui.Dialog()
			dialog.ok(traducao(3005),traducao(3008))
			selfAddon.openSettings()
			return '-'
		lines = []
		try:
			f = open(local_folder+'pdfreader_db.txt',"r")
			lines = f.readlines()
			f.close()
			flag = False
			for line in lines: ## Verifica se ficheiro ja existe
				if 'url="' + url + '"' in line:
					flag = True
					path  = re.compile('path="(.+?)"').findall(line)[0]
					break
			if flag:
				if os.path.isfile(os.path.join(local_folder,path)) is True: return os.path.join(local_folder,path)
				else: ## Caso o ficheiro tenha sido apagado
					f = open(local_folder+'pdfreader_db.txt',"w")
					for line in lines:
						if line != 'path="'+path+'" url="'+url+'"\n': f.write(line)
					f.close()
					return self._download_local(url,name)
		except: pass ## Caso nao exista
		name += '_%d=%d.pdf' % (random.randint(1, 10000), random.randint(1, 10000))
		if not self._download(url,name): return '-'
		f = open(local_folder+'pdfreader_db.txt',"w")
		name = name.replace('"','\'')
		for line in lines:
			f.write(line)
		f.write('path="'+name+'" url="'+url+'"\n')
		f.close()
		return os.path.join(local_folder,name)

	def _download(self,url,name=''):
		if local != 'false':
			if local_folder == '':
				dialog = xbmcgui.Dialog()
				dialog.ok(traducao(3005),traducao(3008))
				selfAddon.openSettings()
				return False
			else: mypath=os.path.join(local_folder,name)
		else: mypath=os.path.join(temp,'temp.pdf')	
		if os.path.isfile(mypath) is True:
			dialog = xbmcgui.Dialog()
			dialog.ok(traducao(3005),traducao(3009))
			return False
		dp = xbmcgui.DialogProgress()
		dp.create('Download')
		start_time = time.time()
		try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: self._dialogdown(nb, bs, fs, dp, start_time))
		except:
			while os.path.exists(mypath): 
				try: os.remove(mypath); break 
				except: pass
			dp.close()
			return False
		dp.close()
		return True

	def _dialogdown(self,numblocks, blocksize, filesize, dp, start_time):
		try:
			percent = min(numblocks * blocksize * 100 / filesize, 100)
			currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
			kbps_speed = numblocks * blocksize / (time.time() - start_time) 
			if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
			else: eta = 0 
			kbps_speed = kbps_speed / 1024 
			total = float(filesize) / (1024 * 1024) 
			mbs = '%.02f MB %s %.02f MB' % (currently_downloaded,traducao(3011), total) 
			e = ' (%.0f Kb/s) ' % kbps_speed 
			tempo = traducao(3010) + ': %02d:%02d' % divmod(eta, 60) 
			dp.update(percent, mbs + e,tempo)
		except: 
			percent = 100 
			dp.update(percent) 
		if dp.iscanceled(): 
			dp.close()
			raise _StopDownloading('Stopped Downloading')

	class _StopDownloading(Exception):
		def __init__(self, value): self.value = value 
		def __str__(self): return repr(self.value)
		
class cbx:
	def cbx_read(self,name,url,videoaddon=False):
		if videoaddon: 
			xbmc.executebuiltin("ActivateWindow(busydialog)")
			xbmc.executebuiltin('XBMC.RunAddon(plugin.image.pdfreader)')
			xbmc.sleep(2000)
			xbmc.executebuiltin("Dialog.Close(busydialog)")
		self.clean_temp()
		xbmc.executebuiltin('XBMC.Extract('+url+','+temp+')')
		xbmc.executebuiltin('XBMC.Container.Update(%s?mode=5&url=%s&name=%s)' % ('plugin://plugin.image.pdfreader/', urllib.quote_plus(url),name))
	
	def _play(self,name,url,folder=temp, page=1):
		for f in os.listdir(folder):
			file_path = os.path.join(folder, f)
			if os.path.isfile(file_path): 
				if thumbs == 'false': self._addPage(traducao(3007)+str(page),file_path,artfolder+str(page)+'.png')
				else: self._addPage(traducao(3007)+str(page),file_path,file_path)
				page += 1
			else: self._play(name,url,file_path,page)
		xbmc.executebuiltin("Container.SetViewMode(500)")
	
	def _addPage(self,name,url,iconimage):
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultImage.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', artfolder + 'black-background.jpg')
		liz.setInfo( type='image', infoLabels={ "Title": name } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		return ok
	
	def clean_temp(self):		#Delete temporary files | If you use pdf and cbx in the same addon, use the cbx.clean_temp() instead of pdf.clean_temp()
		self._clean_temp2()
	
	def _clean_temp2(self,folder=temp):	
		for f in os.listdir(folder):
			file_path = os.path.join(folder, f)
			while os.path.exists(file_path): 
				try: 
					if os.path.isfile(file_path): os.remove(file_path); break 
					else:
						self._clean_temp2(file_path)
						os.rmdir(file_path); break
				except: pass