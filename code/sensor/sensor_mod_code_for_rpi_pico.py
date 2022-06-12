# micropython script for delay mod
# tested on: Raspberry Pico

import rp2
import machine
from machine import ADC
from machine import Timer
import time
from machine import Pin
from machine import PWM

# SETUP PINS
# TODO: Design general pin layout
built_in_led = Pin(0, Pin.OUT) # pin 25 is built-in led
state_signal = Pin(1, Pin.OUT) 

analog_out_pin = Pin(2)
analog_out = PWM(analog_out_pin) # create the PWM object
analog_out.freq(1000) # sets the frequency in Hz for the PWM cycle min 1Hz, max 1kHz

sensor = ADC(27)               # pin 27 for analog signal input
potentiometer = ADC(28)        # pin 28 for analog input
trigger_pin = Pin(13, Pin.IN)  # 13 number pin is input
trigger_pin.init(trigger_pin.IN, trigger_pin.PULL_DOWN)
signal_sent = False
    
def sendPulseSignal():
    global built_in_led
    built_in_led.on()
    time.sleep_ms(50) # TODO: decide the generic pulse width
    built_in_led.off()

def sendStateSignal(_state):
    global state_signal
    if _state == True:
        state_signal.on()
    else:
        state_signal.off()
    
def sendAnalogSignal(_val):
    global analog_out
    analog_out.duty_u16(_val) #  sets the duty cycle as a ratio (duty_u16 / 65535)
    

while True:
    trigger_signal = trigger_pin.value()   # trigger value
    threshold = potentiometer.read_u16()   # read potentiometer value as a raw analog value in the range 0-65535
    signal_value = sensor.read_u16()       # read sensor value
    sendAnalogSignal(signal_value)         # always forward analog value
    
    if signal_value > threshold+500:
        sendStateSignal(True)
        if signal_sent == False:
            sendPulseSignal()
            signal_sent = True
    elif signal_value < threshold-500:
        sendStateSignal(False)
        signal_sent = False

