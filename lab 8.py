import PCF8591 as ADC
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
DO = 17
GPIO.setmode(GPIO.BCM)

###########################################################################

def setup():
    # Setup for dual RGB and touch sensor
    GPIO.setmode(GPIO.BOARD)
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
def led(x):
    if x == 0:
        GPIO.output(Rpin, GPIO.LOW)
    elif x == 1:
        GPIO.output(Rpin, GPIO.HIGH)

# Function to check ambient light condition (darkness)
def is_dark():
    return ADC.read(0) < 100  # Adjust threshold based on your photoresistor readings

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
    global tmp
    touch_input = GPIO.input(TouchPin)
    if touch_input != tmp:
        if touch_input == 0:
            print("Touch detected: Turning LED ON")
            led(1)
        elif touch_input == 1:
            print("Touch detected: Turning LED OFF")
            led(0)
        tmp = touch_input

# Main loop to run the nightlight features
def loop():
    while True:
        handle_touch()  # Check for touch input to control LED

        if is_dark():  # If it's dark, check for motion
            if motion_detected():
                print("Motion detected in darkness: Turning LED ON")
                led(1)
                time.sleep(30)  # Keep the LED on for 30 seconds
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
        loop()
    except KeyboardInterrupt:
        destroy()
