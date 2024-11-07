#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

TouchPin = 11
Rpin   = 13

tmp = 0

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

def Led(x):
    if x == 0:
        GPIO.output(Rpin, 0)
    if x == 1:
        GPIO.output(Rpin, 1)
        
def Print(x):
    global tmp
    if x != tmp:
        if x == 0:
            print("turning off")
            tmp = 0
            
        if x == 1:
            print("detected")
            time.sleep(5)
            
        tmp = x

def loop():
    while True:
        Led(GPIO.input(TouchPin))
        Print(GPIO.input(TouchPin))

def destroy():
    GPIO.output(Rpin, GPIO.HIGH)       # Red led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

