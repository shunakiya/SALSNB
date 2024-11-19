import time
import serial
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import RPi.GPIO as GPIO
import mfrc522

# led for fingeprrint 
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# relay pin 
relayPin = 23

# create an mfrc522 object and hard coded uid's
reader = mfrc522.MFRC522()
tag = "2272152072510"
card = "1632241652103"

# initilization for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# initalizing fingerprint port
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Variable to keep track of the solenoid state
solenoid_state = False

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

###################################r#########################

print("this program is used to test the fingerprint and NFC")
print("waiting for some type of input...")

try:
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
    
    isValidFingerprint = get_fingerprint()
    
    if status == reader.MI_OK:
        result = ''.join(map(str, uid))
        print(f"UID: {result}")

    if (isValidFingerprint or ((str(result) == card or str(result) == tag))):
        solenoid_state = not solenoid_state
        GPIO.output(relayPin, solenoid_state)
        
        print("door opened!")
        
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

############################################################

Traceback (most recent call last):
  File "/home/pi/Desktop/project/prod_code.py", line 28, in <module>
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
  File "/home/pi/.local/lib/python3.7/site-packages/adafruit_fingerprint.py", line 121, in __init__
    if self.verify_password() != OK:
  File "/home/pi/.local/lib/python3.7/site-packages/adafruit_fingerprint.py", line 137, in verify_password
    return self._get_packet(12)[0]
  File "/home/pi/.local/lib/python3.7/site-packages/adafruit_fingerprint.py", line 349, in _get_packet
    raise RuntimeError("Failed to read data from sensor")
RuntimeError: Failed to read data from sensor
