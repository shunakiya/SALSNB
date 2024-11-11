import time
import serial
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# led for fingeprrint 
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# relay pin 
relayPin = 23

# rfid variables
reader = SimpleMFRC522()
card = 703838827623

# initilization for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# initalizing fingerprint port
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

############################################################

print("this program is used to test the fingerprint and RFID")
print("waiting for some type of input...")

if (get_fingerprint() or (reader.read() == card)):
    GPIO.output(relayPin, 1)
    print("door opened!")

############################################################

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
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


