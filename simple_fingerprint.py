import serial
import adafruit_fingerprint
import RPi.GPIO as GPIO
import time

# Relay pin 
relayPin = 23

# Initialization for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

#################################################################

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

#################################################################

try:    
    print("Reading fingerprint...")
    
    while True:
        isValidFingerprint = get_fingerprint()
        
        if isValidFingerprint:
            print(f"Detected # {finger.finger_id}")
            GPIO.output(relayPin, 1)
            time.sleep(1)
            GPIO.output(relayPin, 0)

            break
        else:
            print("Valid fingerprint not detected.")
            break
except Exception as e:
    print(f"Error:{e}")

finally:
    uart.close()
    GPIO.cleanup()
    finger.close_uart()
    print("\nExiting Program.")
