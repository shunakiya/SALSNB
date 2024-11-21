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

# Create an MFRC522 object and hard-coded UID's
reader = mfrc522.MFRC522()
tag = "2272152072510"
card = "1632241652103"

# Initialization for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# Initializing fingerprint port
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# Variable to keep track of the solenoid state
solenoid_state = False

try:
    # Attempt fingerprint initialization
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    finger.soft_reset()  # Reset sensor at the start
except RuntimeError as e:
    print(f"Error initializing fingerprint sensor: {e}")
    uart.close()
    GPIO.cleanup()
    exit(1)


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


print("This program is used to test the fingerprint and NFC")
print("Waiting for some type of input...")

try:
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    isValidFingerprint = get_fingerprint()

    if status == reader.MI_OK:
        result = ''.join(map(str, uid))
        print(f"UID: {result}")

    if isValidFingerprint or ((str(result) == card or str(result) == tag)):
        solenoid_state = not solenoid_state
        GPIO.output(relayPin, solenoid_state)

        print("Door opened!")

        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    # Ensure UART and GPIO cleanup on program exit
    uart.close()
    GPIO.cleanup()
