import time
import serial
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import RPi.GPIO as GPIO

# Relay pin 
relayPin = 23

# Initialization for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# Global variable to track solenoid state
solenoid_state = False

# Initializing fingerprint port
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# Set variable to use later
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
finger.soft_reset()

def toggle_solenoid():
    """Toggle the solenoid state."""
    global solenoid_state
    solenoid_state = not solenoid_state
    GPIO.output(relayPin, solenoid_state)
    print(f"Solenoid {'enabled' if solenoid_state else 'disabled'}")

def get_fingerprint():
    """Get a fingerprint image, template it, and see if it matches."""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'."""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            print("Error during templating")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        print("Error creating model")
        return False

    print(f"Storing model #{location}...", end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        print("Error storing model")
        return False

    return True

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i

try:
    while True:
        print("----------------")
        if finger.read_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to read templates")
        
        print("Fingerprint templates:", finger.templates)
        print("e) enroll print")
        print("f) find print")
        print("d) delete print")
        print("----------------")
        
        c = input("> ")

        if c == "e":
            enroll_finger(get_num())
            
        elif c == "f":
            if get_fingerprint():
                print(f"Detected # {finger.finger_id}")
                toggle_solenoid()  # Toggle the solenoid state on fingerprint recognition
                
            else:
                print("Finger not found")
                
        elif c == "d":
            if finger.delete_model(get_num()) == adafruit_fingerprint.OK:
                print("Deleted!")
            else:
                print("Failed to delete")
                
except KeyboardInterrupt:
    uart.close()
    finger.close_uart()
    GPIO.cleanup()
