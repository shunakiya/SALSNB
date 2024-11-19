   pip install spidev RPi.GPIO mfrc522-python
import RPi.GPIO as GPIO
import mfrc522

# Set up GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Create an MFRC522 reader object
reader = mfrc522.MFRC522(spi_bus=0, spi_device=0, gpio_rst=25) # Adjust GPIO pins as needed

try:
    while True:
        # Check for a card
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status == reader.MI_OK:
            print("Card detected")

            # Get the UID of the card
            (status, uid) = reader.MFRC522_Anticoll()

            if status == reader.MI_OK:
                print("Card read UID: " + str(uid))

except KeyboardInterrupt:
    GPIO.cleanup()
