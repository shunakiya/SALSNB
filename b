import time
import serial
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import RPi.GPIO as GPIO
import mfrc522

# LED for fingerprint
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Relay pin
relayPin = 23

# RFID Reader setup
reader = mfrc522.MFRC522()
tag = "2272152072510"
card = "1632241652103"

# Relay setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# Fingerprint sensor setup
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Solenoid state
solenoid_state = False

def get_fingerprint():
    """Check for a valid fingerprint."""
    print("Waiting for fingerprint...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating fingerprint...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching fingerprint database...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def get_rfid():
    """Check for a valid RFID tag."""
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
    if status == reader.MI_OK:
        (status, uid) = reader.MFRC522_Anticoll()
        if status == reader.MI_OK:
            return ''.join(map(str, uid))
    return None

def unlock_door():
    """Activate the solenoid to unlock the door."""
    global solenoid_state
    solenoid_state = not solenoid_state
    GPIO.output(relayPin, solenoid_state)
    print("Door unlocked!")
    time.sleep(1)

print("System ready: Waiting for fingerprint or RFID input...")

try:
    while True:
        # Check fingerprint
        isValidFingerprint = get_fingerprint()

        # Check RFID
        rfid_tag = get_rfid()

        # Validate and unlock door
        if isValidFingerprint or (rfid_tag and rfid_tag in [card, tag]):
            unlock_door()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nExiting program.")
