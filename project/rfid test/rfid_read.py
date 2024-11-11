import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    id,  uid = reader.read()
    print(id)
    print(uid)
finally:
    GPIO.cleanup()