# coding=UTF-8
import os

DEFAULT_MEDIA_PATH = "/media/pi/"


def cleanPath(path):
	if path == "":
		return ""
	path = path.strip('\"')
	path = os.path.abspath(path)
	path = "\"" + path + "\""
	return path


# Palauta True jos annettu tiedosto on kansio tai piilotiedosto.
# Palauta True myös jos lukeminen ei onnistu (esim. oikeuksien takia)
# Return True if the given path is a directory or hidden file.
# Also return True if reading fails (eg. because of permissions)
def isDirectoryOrHiddenFile(path):
	try:
		if os.path.isdir(path):
			print path + " on kansio"
			return True
		filename = os.path.basename(path)
		if filename[0] == ".":
			print cleanPath(path) + " on piilotiedosto"
			return True
		print cleanPath(path) + " on tiedosto"
		return False
	except:
		print "Ei voitu lukea: " + path+filename
		print "Could not read file " + path+filename
		return True


class mediaLoader:
	
	# Mistä etsitään liitettyjä medialaitteita. Oletus: /media/pi/
	# Where to look for mounted media devices. Default: /media/pi/
	mediaMountPath = DEFAULT_MEDIA_PATH
	
	
	# This is set when media file is found, so the media can be unmounted
	# Tämä asetetaan kun mediatiedosto löytyy, jotta media voidaan irrottaa
	pathToUnmount = ""
	
	
	def setMediaMountPath(self, path):
		self.mediaMountPath = path
		
	
	# Poista hakemisto
	# Remove the directory at 'path'
	def removeDir(self, path):
		path = cleanPath(path)
		rmCommand = "rm -rfv " + path
		try:
			os.system(rmCommand)
		except:
			print "Ei voitu poistaa: " + path
			print "Could not remove: " + path
	
	
	# Palauta koko polku ensimmäiseen löytyvään tiedostoon annetussa polussa. 
	#   Palauta "" jos ei löydy tiedostoa, tai jos tulee muu virhe.
	# Return the full path to the first file found at the given path.
	#   Return "" if there are no files in the path, or on other error.
	def getFilenameFromPath(self, path):
		try:
			files = os.listdir(path)
		except:
			print "Ei voitu lukea: " + path
			print "Could not read: " + path
			return ""
		
		if len(files) == 0:
			return ""
		files.sort()
		
		for filename in files:
			if isDirectoryOrHiddenFile(path + "/" + filename):
				continue
			else:
				return path + "/" + filename
		
		return ""	
	
	
	# Palauta koko polku ensimmäiseen medialta löytyvään tiedostoon. 
	#   Palauta "" jos ei löydy tiedostoa, tai jos tulee muu virhe.
	# Return the full path to the first file found at the media.
	#   Return "" if there are no files in the path, or on other error.
	def getFilenameFromMedia(self):
		try:
			mediaList = os.listdir(self.mediaMountPath)
		except:
			print "Ei voitu lukea: " + cleanPath(self.mediaMountPath)
			print "Could not read: " + cleanPath(self.mediaMountPath)
			return ""
		
		if len(mediaList) == 0:
			return ""
		
		for media in mediaList:
			path = self.mediaMountPath + media
			try:
				if os.path.isdir(path) == False:
					print cleanPath(path) + " ei ole kansio"
					print cleanPath(path) + " is not a directory"
					continue
				files = os.listdir(path)
			except:
				continue
			if len(files) == 0:
				continue
			files.sort()
			for filename in files:
				if isDirectoryOrHiddenFile(path + "/" + filename):
					continue
				else:
					self.pathToUnmount = path
					return path + "/" + filename
		return ""


	# Huom. tämä poistaa kaiken dstPath:sta!
	# Palauta True jos tiedosto kopioitiin
	# Note: This removes all files from dstPath!
	# Return True if file was copied
	def copyFromMediaToPath_removeOld(self, dstPath):

		filenameFromMedia = cleanPath(self.getFilenameFromMedia())
		dstPath = cleanPath(dstPath)
		
		if filenameFromMedia == "":
			return False
		
		print "Poistetaan " + dstPath
		print "Removing " + dstPath
		self.removeDir(dstPath)
		
		print 	"Kopioidaan " + filenameFromMedia + " -> " + dstPath
		print 	"Copying " + filenameFromMedia + " -> " + dstPath
		
		try:
			cpCommand = "cp -v "  + filenameFromMedia + " " + dstPath + "/"
			
			# varmista että kansio on olemassa
			# make sure the directory exists
			mkdirCommand = "mkdir -p " + dstPath
			
			os.system(mkdirCommand)
			os.system(cpCommand)
			
		except:
			print "Kopiointi epäonnistui"
			print "Copying failed"
			return False
		
		return True

	
	def unmount(self):
		if self.pathToUnmount == "":
			return
		try:
			os.system("umount " + cleanPath(self.pathToUnmount) )
		except:
			print "Ei voitu irrottaa: " + self.pathToUnmount
			print "Could not unmount: " + self.pathToUnmount
			return
