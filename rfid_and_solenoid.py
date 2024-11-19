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

# variable for toggling loop
isReading = True

try:
    while isReading:
        # Check for a card
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            # Get the UID of the card
            (status, uid) = reader.MFRC522_Anticoll()

            if status == reader.MI_OK:
                result = ''.join(map(str, uid))
                print(result)
                
                GPIO.output(relayPin, 1)
                time.sleep(1)
                GPIO.output(relayPin, 0)

                isReading = False

except KeyboardInterrupt:
    GPIO.cleanup()
