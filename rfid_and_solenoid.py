import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

relayPin = 23

# initilization for relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

try:
    id,  uid = reader.read()
    print(id)
    print(uid)
    
    GPIO.output(relayPin, 1)
    time.sleep(1)
    GPIO.output(relayPin, 0)
    
finally:
    GPIO.cleanup()

/home/pi/.local/lib/python3.7/site-packages/mfrc522/MFRC522.py:151: RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
  GPIO.setup(pin_rst, GPIO.OUT)
Traceback (most recent call last):
  File "/home/pi/Desktop/project/rfid test/rfid_read.py", line 10, in <module>
    GPIO.setmode(GPIO.BCM)
ValueError: A different mode has already been set!
>>> 
