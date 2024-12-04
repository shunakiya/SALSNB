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

tag = "2272152072510"
card = "1632241652103"

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
                print(f"UID: {result}")
                
                if(str(result) == card or str(result) == tag):
                    # Toggle the solenoid state
                    print("uid recognized")
                    solenoid_state = not solenoid_state
                    GPIO.output(relayPin, solenoid_state)
                else:
                    print("uid not recognized")
                    break
                
                # Wait a bit to avoid multiple reads of the same card
                time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated.")
    GPIO.cleanup()