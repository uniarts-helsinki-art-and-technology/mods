#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os

from omxplayer.player import OMXPlayer
from time import sleep

from pynput import mouse

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ledPin = 12
buttonPin = 16

swichPin = 7

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(swichPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

VIDEO_PATH = ""

transparency = 1.0

def on_move(x, y):
    #print(x, y)
    global transparency
    if(x < 150 and y > 900):
        transparency = 1.0;
        #print("transparent " + str(transparency))
    else:        
        transparency = 0.5
        #print("opaque" + str(transparency))


 

class mods_playVideoWithTrigger:    

    os.system("killall omxplayer.bin")
    
    global transparency
    
    alpha = 1
    listener = mouse.Listener(on_move=on_move)
    listener.start()
    
    def setPath(self, path):
        
        VIDEO_PATH = path
        print("VIDEO_PATH is " + VIDEO_PATH)    
   
        # setup omxplayer
        
        #VIDEO_PATH = "/home/pi/Desktop/videot/The Simpsons Movie - 1080p Trailer.mp4"        

        adev='local'
        # remember hdmi closest to usb-c power
        #adev='hdmi'
                
        player = OMXPlayer(VIDEO_PATH, args=['--no-osd', '--no-keys', '--win', '50 50 640 480', '--loop', '-o', adev], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
        sleep(1.5)
        #player.set_video_pos(200, 200, 800, 699)
        player.pause()
        player.set_position(0)
        
        player.set_video_pos(0, 0, 1920, 1080)
        # it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3
        
        duration = player.duration()
        print(duration)
        sleep(3.5)
        player.play()
        
        prevSwitchState = 1
        
        while True:
            
            
            if(transparency == 0.5 and self.alpha == 1):
                player.set_alpha(255*transparency)
                self.alpha = transparency
                print("transparency " + str(transparency))
                print("alpha " + str(self.alpha))
                player.set_video_pos(50, 50, 640, 360)
            elif (transparency == 1 and self.alpha == 0.5):
                player.set_alpha(255)
                self.alpha = 1
                print("transparency " + str(transparency))
                print("alpha " + str(self.alpha))
                player.set_video_pos(0, 0, 1920, 1080)
            
            buttonState = GPIO.input(buttonPin)
            switchState = GPIO.input(swichPin)
            #print("trying to play file")
            
            if switchState == 1:
                #print("trigger mode active")
                
                if prevSwitchState == 0:
                    print("trigger mode activated")
                    prevSwitchState = 1
                
                if (buttonState == False and player.playback_status() != "Playing"):
                    print("trigger mode active")
                    GPIO.output(ledPin, GPIO.HIGH)
                    player.set_alpha(255*transparency)
                    player.play()
                else:
                    GPIO.output(ledPin, GPIO.LOW)
                    
                if player.playback_status() == "Playing":
                    #player.set_alpha(player.position()*25)
                    #print(player.position())
                    if player.position() > duration - 1:
                        player.set_alpha(0)
                        sleep(1)
                        player.pause()
                        player.set_position(0)
                        sleep(1)
                        
            else:
                #print("loop")
                if prevSwitchState == 1:
                    print("loop mode activated")
                    prevSwitchState = 0
                if (player.playback_status() != "Playing"):
                    print("loop mode")
                    player.set_position(0)
                    player.set_alpha(255*transparency)
                    player.play()
