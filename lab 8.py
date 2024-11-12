import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

# Pins for touch and dual RGB LED (physical pin numbers)
TouchPin = 11  # Pin 11 corresponds to GPIO 17 in BOARD mode
Rpin = 13      # Pin 13 corresponds to GPIO 27
Bpin = 15      # Pin 15 corresponds to GPIO 22 (optional creative feature)

# Pins for ultrasonic sensor (physical pin numbers)
TRIG = 33      # Pin 33 corresponds to GPIO 13
ECHO = 32      # Pin 32 corresponds to GPIO 12

# Pin for photoresistor and PCF8591 (physical pin number)
DO = 18        # Pin 18 corresponds to GPIO 24

# Global variable to track LED state
led_state = False  # Initially off

###########################################################################

def setup():
    # Setup GPIO mode to BOARD (physical pin numbering)
    GPIO.setmode(GPIO.BOARD)
    
    # Setup for dual RGB and touch sensor
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(Bpin, GPIO.OUT)  # Setup for Blue LED (optional)
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Setup for ultrasonic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # Setup for PCF8591 and photoresistor
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)  # Setup as input for the photoresistor's digital output

###########################################################################

# Function to control LED (on/off based on input)
def led(state):
    GPIO.output(Rpin, GPIO.HIGH if state else GPIO.LOW)

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

# Function to toggle the LED state when touch sensor is pressed
def handle_touch():
    global led_state
    if GPIO.input(TouchPin) == GPIO.LOW:  # Touch detected (assuming active low)
        led_state = not led_state  # Toggle the LED state
        led(led_state)  # Update the LED based on the new state
        print("Touch detected: LED is now", "ON" if led_state else "OFF")
        time.sleep(0.5)  # Debounce delay

# Main loop to run the nightlight features
def loop():
    while True:
        handle_touch()  # Check for touch input to toggle LED

        if is_dark():  # If it's dark, check for motion
            if motion_detected():
                print("Motion detected in darkness: Turning LED ON")
                led(True)
                time.sleep(30)  # Keep the LED on for 30 seconds
                led(False)
                print("Auto shut-off after 30 seconds")

        time.sleep(0.1)

# Function to turn off LED and clean up GPIO
def destroy():
    led(False)  # Turn off LED
    GPIO.cleanup()

###########################################################################

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
