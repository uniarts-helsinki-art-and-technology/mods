#!/usr/bin/python -u
#coding=UTF-8

#	Toista USB-tikulta videotiedosto omxplayerilla
#	Play a video file from USB drive with omxplayer

#	Lisenssi: GNU GPL
#	License: GNU GPL

from mediaLoader import mediaLoader
from mediaLoader import cleanPath
from mods_playVideoWithTrigger import mods_playVideoWithTrigger

import os
import time
import sys



localPath = "/home/pi/Desktop/videot"
mediaPath = "/media/pi/"
maxTries = 3

# for clean shutdown uncomment next line and set time in minutes
#os.system("shutdown -h 360")

loader = mediaLoader()
loader.setMediaMountPath(mediaPath)


def playVideo(path):
	try:
		playVideoWithTrigger = mods_playVideoWithTrigger()
		playVideoWithTrigger.setPath(path)
        
	except:
		print "Toistaminen epäonnistui: " + path
		print "Failed to play file " + path


# Yritä 'maxTries' kertaa kopioida USB-medialta tiedostoa.
# Jos ei löydy, toista lokaalista polusta.
# Jos lokaalista polustakaan ei löydy, yritä uudelleen loputtomasti.
print "Haetaan tiedostoa USB-medialta polusta " + cleanPath(mediaPath)
print "Searching for file from USB media in path " + cleanPath(mediaPath)
fileWasCopied = loader.copyFromMediaToPath_removeOld(localPath)


try_i = 0
while fileWasCopied == False and try_i < maxTries:
	try_i = try_i + 1
	print "Yritetään uudestaan... " + str(try_i) + "/" + str(maxTries)
	print "Trying again... "
	time.sleep(1)
	fileWasCopied = loader.copyFromMediaToPath_removeOld(localPath)

if fileWasCopied == True:
	print "Tiedosto kopioitiin"
	print "File was copied"
	loader.unmount()
	# Viive on sitä varten että käyttäjä ehtii lukea tekstipäätteen
	# Sleep so that the user has time to read the text terminal
	time.sleep(5)
else:
	print "Ei löydetty tiedostoa USB-medialta polussa " + cleanPath(mediaPath)
	print "No file found on USB media in path " + cleanPath(mediaPath)

localFile = loader.getFilenameFromPath(localPath)
print("local file " + localFile)

if localFile == "":
	print "Ei löydetty tiedostoa polusta " + localPath
	print "No file found at " + localPath	
		
	# Jos toisto keskeytyy, aloitetaan heti uudestaan
	# If playback is interrupted, start again immediately
else:
    playVideo(localFile)
    time.sleep(1)

