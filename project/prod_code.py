import threading
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
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

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
unlock_event = threading.Event()

#########################################################################

def reset_fingerprint_sensor():
    """Reset the fingerprint sensor and reinitialize communication."""
    print("Resetting fingerprint sensor...")
    try:
        finger.soft_reset()
        time.sleep(1)
    except Exception as e:
        print(f"Error during sensor reset: {e}")

#########################################################################

def fingerprint_thread():
    """Thread to check for valid fingerprint."""
    while True:
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

                print("Fingerprint matched!")
                unlock_event.set()  # Signal to unlock the door
                return
            except RuntimeError as e:
                print(f"Error: {e}. Retrying...")
                reset_fingerprint_sensor()

        print("Failed to get a valid fingerprint after 3 attempts.")
        time.sleep(1)  # Avoid busy waiting

#########################################################################

def rfid_thread():
    """Thread to check for valid NFC UID."""
    while True:
        print("Waiting for RFID card...")
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status == reader.MI_OK:
            (status, uid) = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                rfid_uid = ''.join(map(str, uid))
                print(f"RFID detected: {rfid_uid}")
                if rfid_uid in [tag, card]:
                    print("RFID matched!")
                    unlock_event.set()  # Signal to unlock the door
                    return
        time.sleep(0.5)  # Avoid busy waiting

#########################################################################

def unlock_door():
    """Activate the solenoid to unlock the door."""
    global solenoid_state
    solenoid_state = True
    GPIO.output(relayPin, solenoid_state)
    print("Door unlocked!")
    time.sleep(5)  # Keep door unlocked for 5 seconds
    solenoid_state = False
    GPIO.output(relayPin, solenoid_state)
    print("Door locked.")

#########################################################################

# Main program
print("Waiting for fingerprint or NFC input...")

try:
    while True:
        # Start threads for fingerprint and RFID
        fingerprint_t = threading.Thread(target=fingerprint_thread)
        rfid_t = threading.Thread(target=rfid_thread)
        
        # Start both threads
        fingerprint_t.start()
        rfid_t.start()
        
        # Wait for either thread to signal an unlock event
        unlock_event.wait()

        # Unlock the door
        unlock_door()

        # Clear the unlock event
        unlock_event.clear()

        # Ensure threads finish before restarting
        fingerprint_t.join()
        rfid_t.join()
except KeyboardInterrupt:
    GPIO.cleanup()
    uart.close()
    print("\nExiting program.")