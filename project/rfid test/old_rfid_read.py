import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    id,  uid = reader.read()
    print(id)
    print(uid)
    
except Exception as e:
    print("An error has occured:", e)
    
finally:
    GPIO.cleanup()