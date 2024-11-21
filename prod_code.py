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

# relay pin
relayPin = 23

# fingerprint sensor setup
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

try:  
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    finger.soft_reset()
    
except RuntimeError as e:
    print(f"Error initalizing fingerprint sensor: {e}")
    
    GPIO.cleanup()
    uart.close()
    finger.close_uart()
    
    print("\nExiting program.")
    exit(1)
    
# NFC reader setup
reader = mfrc522.MFRC522()
tag = "2272152072510"
card = "1632241652103"

# relay setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# solenoid state
solenoid_state = False

#########################################################################

def get_fingerprint():
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
    
    print("Failed to get a valid fingerprint.")
    return False

#########################################################################

def get_rfid():
    # check for a valid NFC uid
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
    
    if status == reader.MI_OK:
        (status, uid) = reader.MFRC522_Anticoll()
        
        if status == reader.MI_OK:
            return ''.join(map(str, uid))
        
    return None

#########################################################################

def unlock_door():
    # activate the solenoid to unlock door
    global solenoid_state
    
    solenoid_state = not solenoid_state
    GPIO.output(relayPin, solenoid_state)
    
    print("Door unlocked!")
    time.sleep(1)

#########################################################################
# main program

print("Waiting for fingerprint or NFC input...")

try:
    while True:
        # check fingerprint
        isValidFingerprint = get_fingerprint()

        # check nfc
        rfid_tag = get_rfid()

        # validate authentication and unlock door
        if isValidFingerprint or (rfid_tag and rfid_tag in [card, tag]):
            unlock_door()

except KeyboardInterrupt:
    GPIO.cleanup()
    uart.close()
    finger.close_uart()
    print("\nExiting program.")

Waiting for fingerprint or NFC input...
Waiting for fingerprint...
Traceback (most recent call last):
  File "/home/pi/Desktop/project/prod_code.py", line 101, in <module>
    isValidFingerprint = get_fingerprint()
  File "/home/pi/Desktop/project/prod_code.py", line 52, in get_fingerprint
    while finger.get_image() != adafruit_fingerprint.OK:
  File "/home/pi/.local/lib/python3.7/site-packages/adafruit_fingerprint.py", line 180, in get_image
    return self._get_packet(12)[0]
  File "/home/pi/.local/lib/python3.7/site-packages/adafruit_fingerprint.py", line 349, in _get_packet
    raise RuntimeError("Failed to read data from sensor")
RuntimeError: Failed to read data from sensor
