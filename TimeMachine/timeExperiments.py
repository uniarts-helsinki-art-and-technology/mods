import machine
import utime
import time

rampTime = 4000
sustainTime = 4000
delayTime = 10000

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_red = machine.Pin(15, machine.Pin.OUT)

def createEnvelope():
    print("start")
    print("delay started")
    time.sleep(delayTime/1000)
    print("delay ended")
    timer_start = time.ticks_ms()
    attackEnded = False
    print("attack started")
    while attackEnded == False:
        attack = time.ticks_diff(time.ticks_ms(), timer_start)
        value = attack/rampTime
        #print(value)
        if value >= 1:
            attackEnded = True
            value = 1
        led_red.value(value)
    print("attack ended")
    print("sustain started")
    led_onboard.value(1)
    time.sleep(sustainTime/1000)
    led_onboard.value(0)
    print("sustain ended")
    releaseEnded = False
    timer_start = time.ticks_ms()
    print("release started")
    while releaseEnded == False:
        release = time.ticks_diff(time.ticks_ms(), timer_start)
        value = 1 - release/rampTime
        #print(value)
        if value <= 0:
            releaseEnded = True
            value = 0
        led_red.value(value)
    print("release ended")
    
while(True):
    createEnvelope()   