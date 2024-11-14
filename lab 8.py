# necessary imports
import PCF8591 as ADC
import smbus2
import RPi.GPIO as GPIO
import time

# pins for touch and dual rgb led
TouchPin = 11
Rpin = 13
tmp = 0

# pins for ultrasonic
TRIG = 33
ECHO = 32

# pins for photoresistor and pcf8591
DO = 24

# global variable to track led
led_state = 0

###########################################################################
def setup():
    # settings pins to board mode
    GPIO.setmode(GPIO.BOARD)
    
    # setup for dual rgb and touch sensor
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # setup for photoresistor and PCF8591
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)

###########################################################################
# function to control dual rgb led (on and off)
def led(state):
    # 0 and on and 1 is off
    if state == 0:
        GPIO.output(Rpin, 1)
    elif state == 1:
        GPIO.output(Rpin, 0)

# function to check for light
def is_dark():
    return ADC.read(0)

# function to check motion with ultrasonic sensor
def motion_detected():
    distance = get_distance()
    # return if motion is detected if an object is within 50 cm
    return distance < 50 

# function to get distance from ultrasonic sensor
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.000002)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # t initial of when motion is in front of sensor
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # t final of when motion leaves sensor
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # pulse_duration = delta t
    pulse_duration = pulse_end - pulse_start
    
    # math logic to convert sound (343 m/s) to cm
    distance = pulse_duration * 17150
    
    return distance

# function to handle touch sensor 
def handle_touch():
    global led_state, tmp

    # set variable for touch input
    touch_input = GPIO.input(TouchPin)

    # t flip flop logic for toggling led on and off with touch sensor
    if touch_input == 1 and tmp == 0:
        led_state = 1 - led_state
        led(led_state)
    
    if led_state == 1:
        print("Touch detected: LED ON")
    else:
        print("Touch detected: LED OFF")
    
    time.sleep(0.2)

# main loop to run in main
def loop():
    while True
        # check for touch input to control led
        handle_touch()

        # if dark, check for motion (6 is light, 7 is dark)
        if is_dark() == 7:
            if motion_detected():
                print("Motion detected: LED ON")
                
                led(1)
                # keep led on for 30 seconds
                time.sleep(30)
                led(0)
                
                print("Auto shut-off after 30 seconds")

        time.sleep(0.1)

# function to turn off LED and clean up GPIO
def destroy():
    led(0) 
    GPIO.cleanup()

###########################################################################
# main program
if __name__ == '__main__':
    setup()
    try:
        # ignore GPIO errors
        GPIO.setwarnings(False)

        # main program runs forever unless 'ctrl + c' is pressed
        loop()
    except KeyboardInterrupt:
        destroy()

