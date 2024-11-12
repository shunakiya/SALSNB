# relevant imports
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import signal

# pins for touch and dual rgb led
TouchPin = 11
Rpin = 13
tmp = 0

# pins for ultrasonic sensor
TRIG = 33
ECHO = 32

# pins for photoresistor and pcf8591
DO = 17
GPIO.setmode(GPIO.BCM)

# Global variables
led_state = False
motion_timer = None

def setup():
    # setup for dual rgb and touch sensor
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # set up for pcf8591 and photoresistor
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)

    # Setup interrupt for touch sensor
    GPIO.add_event_detect(TouchPin, GPIO.FALLING, callback=touch_callback, bouncetime=300)

def touch_callback(channel):
    global led_state, motion_timer
    led_state = not led_state
    led(led_state)
    print("LED turned", "on" if led_state else "off", "by touch")
    if motion_timer:
        motion_timer.cancel()
        motion_timer = None

def led(state):
    GPIO.output(Rpin, state)

def is_dark():
    # Read light level from photoresistor
    light_level = ADC.read(0)
    # Adjust this threshold as needed
    return light_level < 100  # Example threshold

def motion_detected():
    dis = distance()
    # Adjust this threshold as needed
    return dis < 100  # Example: motion detected if distance less than 100 cm

def auto_shutoff():
    global led_state, motion_timer
    led_state = False
    led(led_state)
    print("LED auto shut-off after 30 seconds")
    motion_timer = None

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

def loop():
    global led_state, motion_timer
    while True:
        if is_dark() and motion_detected() and not led_state:
            led_state = True
            led(led_state)
            print("Motion detected in darkness, LED turned on")
            if motion_timer:
                motion_timer.cancel()
            motion_timer = Timer(30, auto_shutoff)
            motion_timer.start()
        
        time.sleep(0.1)  # Small delay to prevent CPU overuse

def destroy():
    GPIO.output(Rpin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt: 
        destroy()
