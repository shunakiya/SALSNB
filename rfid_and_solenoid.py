import RPi.GPIO as GPIO
import mfrc522
import time

relayPin = 23

# Set up GPIO mode to BCM
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

# Create an MFRC522 reader object
reader = mfrc522.MFRC522()

# Variable to keep track of the solenoid state
solenoid_state = False

try:
    while True:
        # Check for a card
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            # Get the UID of the card
            (status, uid) = reader.MFRC522_Anticoll()

            if status == reader.MI_OK:
                result = ''.join(map(str, uid))
                print(f"Card detected. UID: {result}")
                
                # Toggle the solenoid state
                solenoid_state = not solenoid_state
                GPIO.output(relayPin, solenoid_state)
                
                print(f"Solenoid {'activated' if solenoid_state else 'deactivated'}")
                
                # Wait a bit to avoid multiple reads of the same card
                time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated.")
    GPIO.cleanup()
