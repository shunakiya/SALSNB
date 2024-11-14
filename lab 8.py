import PCF8591 as ADC
import smbus2
import RPi.GPIO as GPIO
import time

# Pins for touch and dual RGB LED
TouchPin = 11
Rpin = 13
Bpin = 15  # Added Blue LED pin for additional creative feature (optional)
tmp = 0

# Pins for ultrasonic sensor
TRIG = 33
ECHO = 32

# Pins for photoresistor and PCF8591
DO = 24

# global variable to track led
led_state = 0

###########################################################################

def setup():
    
    GPIO.setmode(GPIO.BOARD)
    
    # Setup for dual RGB and touch sensor
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(Bpin, GPIO.OUT)  # Setup for Blue LED
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # Setup for PCF8591 and photoresistor
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)

###########################################################################

# Function to control LED (on/off based on input)
def led(state):
    if state == 0: # if the led is on, then:
        GPIO.output(Rpin, 1) # turns off led
    elif state == 1: # if the led is off, then:
        GPIO.output(Rpin, 0) # turns on led

# Function to check ambient light condition (darkness)
def is_dark():
    return ADC.read(0) # Adjust threshold based on your photoresistor readings

# Function to check motion using ultrasonic sensor
def motion_detected():
    distance = get_distance()
    return distance < 50  # Motion detected if object is within 50 cm

# Function to get distance from ultrasonic sensor
def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.000002)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 343 m/s, convert to cm
    return distance

# Function to handle touch sensor input
def handle_touch():
    global led_state, tmp
    
    touch_input = GPIO.input(TouchPin)
    
    if touch_input == 1 and tmp == 0:
        led_state = 1 - led_state
        led(led_state)
        
    if led_state == 1:
        print("Touch detected: LED ON")
    else:
        print("Touch detected: LED OFF")
    
    time.sleep(0.2)

# Main loop to run the nightlight features
def loop():
    while True:
        handle_touch()  # Check for touch input to control LED

        if is_dark() == 7:  # If it's dark, check for motion
            if motion_detected():
                print("Motion detected in darkness: Turning LED ON")
                led(1)
                time.sleep(5)  # Keep the LED on for 30 seconds
                led(0)
                print("Auto shut-off after 30 seconds")

        time.sleep(0.1)

# Function to turn off LED and clean up GPIO
def destroy():
    led(0)  # Turn off LED
    GPIO.cleanup()

###########################################################################

if __name__ == '__main__':
    setup()
    try:
        GPIO.setwarnings(False)
        loop()
    except KeyboardInterrupt:
        destroy()

