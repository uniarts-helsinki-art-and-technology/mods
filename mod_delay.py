# micropython script for delay mod
# tested on: Raspberry Pico

import rp2
import machine
from machine import ADC
import time

from machine import Pin

built_in_led = Pin(0, Pin.OUT) # pin 25 is built-in led
potentiometer = ADC(28)        # pin 28 for analog input
trigger_pin = Pin(13, Pin.IN)  # 13 number pin is input
trigger_pin.init(trigger_pin.IN, trigger_pin.PULL_DOWN)
state = False

while True:
    logic_state = trigger_pin.value()  # trigger value
    if logic_state == True and state == False:
        delay = potentiometer.read_u16()   # input potentiometer value
        time.sleep_ms(delay)
        built_in_led.on()
        time.sleep_ms(50) # 50 ms, TODO: decide the generic pulse width
        state = True
    else:
        built_in_led.off()
        state = False

    
