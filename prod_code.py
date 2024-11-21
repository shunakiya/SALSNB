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

# Fingerprint sensor setup
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

try:  
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    finger.soft_reset()
except RuntimeError as e:
    print(f"Error initializing fingerprint sensor: {e}")
    GPIO.cleanup()
    uart.close()
    exit(1)

# NFC reader setup
reader = mfrc522.MFRC522()
tag = "2272152072510"
card = "1632241652103"

# Relay setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# Solenoid state
solenoid_state = False

#########################################################################
def reset_fingerprint_sensor():
    """Reset the fingerprint sensor and reinitialize communication."""
    print("Resetting fingerprint sensor...")
    try:
        finger.soft_reset()
        time.sleep(1)
    except Exception as e:
        print(f"Error during sensor reset: {e}")

def get_fingerprint():
    """Check for a valid fingerprint."""
    print("Waiting for fingerprint...")
    for attempt in range(3):  # Retry up to 3 times
        try:
            while finger.get_image() != adafruit_fingerprint.OK:
                pass
            
            print("Templating fingerprint...")
            if finger.image_2_tz(1) != adafruit_fingerprint.OK:
                raise RuntimeError("Templating failed")
            
            print("Searching fingerprint database...")
            if finger.finger_search() != adafruit_fingerprint.OK:
                raise RuntimeError("Search failed")
            
            return True
        except RuntimeError as e:
            print(f"Error: {e}. Retrying...")
            reset_fingerprint_sensor()
    
    print("Failed to get a valid fingerprint after 3 attempts.")
    return False

def get_rfid():
    """Check for a valid NFC UID."""
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

#########################################################################
# Main program
print("Waiting for fingerprint or NFC input...")

try:
    while True:
        # Check fingerprint
        isValidFingerprint = get_fingerprint()

        # Check NFC
        rfid_tag = get_rfid()

        # Validate and unlock door
        if isValidFingerprint or (rfid_tag and rfid_tag in [card, tag]):
            unlock_door()
except KeyboardInterrupt:
    GPIO.cleanup()
    uart.close()
    print("\nExiting program.")
