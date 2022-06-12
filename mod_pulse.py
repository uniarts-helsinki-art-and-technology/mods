# micropython script for delay mod
# tested on: Raspberry Pico

import rp2
import machine
from machine import ADC
from machine import Timer
import time
from machine import Pin

# SETUP PINS
built_in_led = Pin(0, Pin.OUT) # pin 25 is built-in led
potentiometer = ADC(28)        # pin 28 for analog input

timer_is_running = False

def sendSignal(s):
    global timer_is_running
    built_in_led.on()
    time.sleep_ms(50) # 50 ms, TODO: decide the generic pulse width
    built_in_led.off()
    timer_is_running = False


while True:
    if timer_is_running == False:
        delay = potentiometer.read_u16()   # input potentiometer value
        tim = Timer(period=delay, mode=Timer.ONE_SHOT, callback=sendSignal) # init timer
        timer_is_running = True
