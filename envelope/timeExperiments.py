import machine
import utime
import time

rampTime = 4000
sustainTime = 4000
delayTime = 10000

rampPin = machine.ADC(28)
sustainPin = machine.ADC(27)
delayPin = machine.ADC(26)

#this is the external state signal
pressed = False
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

led_onboard = machine.Pin(25, machine.Pin.OUT)
led = machine.PWM(machine.Pin(15))
led.freq(1000)

def button_handler(pin):
    utime.sleep_ms(100)
    global pressed
    print("anyway")    

    if not pressed:
        pressed=True
        readAnalogPins()
        createEnvelope()
        print(pin)

def createEnvelope():
    print("start")
    print("delay started with delay " + str(delayTime))
    time.sleep(delayTime/1000)
    print("delay ended")
    timer_start = time.ticks_ms()
    attackEnded = False
    print("attack started with attack time " + str(rampTime))
    while attackEnded == False:
        attack = time.ticks_diff(time.ticks_ms(), timer_start)
        value = attack/rampTime
        #print(value)
        if value >= 1:
            attackEnded = True
            value = 1
        # we go back to 16bits
        led.duty_u16(int(value * 65535))
    print("attack ended")
    print("sustain started with sustain time " + str(sustainTime))
    led_onboard.value(1)
    time.sleep(sustainTime/1000)
    led_onboard.value(0)
    print("sustain ended")
    releaseEnded = False
    timer_start = time.ticks_ms()
    print("release started with release time " + str(rampTime))
    while releaseEnded == False:
        release = time.ticks_diff(time.ticks_ms(), timer_start)
        value = 1 - release/rampTime
        #print(value)
        if value <= 0:
            releaseEnded = True
            value = 0
            led.duty_u16(0)
        else:
            led.duty_u16(int(value * 65535))
    print("release ended")
    global pressed
    pressed = False

def readAnalogPins():
    global rampTime
    global sustainTime
    global delayTime
    rampTime = (rampPin.read_u16() * 10000/65535) + 1
    #print("rampTime " + str(rampTime))
    sustainTime = (sustainPin.read_u16() * 10000/65535) + 1
    #print("sustainTime " + str(sustainTime))
    delayTime = (delayPin.read_u16() * 10000/65535) + 1
    #print("delayTime " + str(delayTime))
    
#while(True):
    

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)