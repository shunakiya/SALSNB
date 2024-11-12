# relavant imports
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

# pins for touch and dual rgb led
TouchPin = 11
Rpin = 13
tmp = 0

# pins for ultrasonic sensor
TRIG = 33
ECHO = 32


# pins for photoresistor and pcf8591
DO = 17
GPIO.setmode(GPIO.BCM)

###########################################################################

def setup():
    # setup for dual rgb and touch sensor
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # setup for ultraosnic sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    # set up for pcf8591 qand photoresistor
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)

###########################################################################

# main program, starts here
if __name__ == '__main__':
    # running initial setup in the beginning of the program

    setup()
    
    try:
        loop()
        
    # if ctrl + c is pressed, terminals the program and ends
    except KeyboardInterrupt: 
        destroy()

###########################################################################3

# function for led changing, defeault is off 
def led(x):
    if x == 0:
        GPIO.output(Rpin, 0)
    if x == 1:
        GPIO.output(Rpin, 1)

# function for printing the touch detection, then turns on rgb led
def print(x):
    global tmp
    
    if x != tmp:
        if x == 0:
            print("turning off")
            tmp = 0
            
        if x == 1:
            print("detected")
            time.sleep(5)
            
        tmp = x

# function that's a while loop, constantly running the main program
def loop():
    while True:
        if(DC.read(0) == 7):
            print("bruh")
        #led(GPIO.input(TouchPin))
        #print(GPIO.input(TouchPin))

# function for getting object distance and logic for calcualting cm
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * (340 / 2) * 100

# function for returning the distaance of ultraosnic sensor
def returnDistance():
    while True:
        dis = distance()
        
        time.sleep(0.1)
        
        if(dis >= 5):
            return 1
        

# function for turning off led and releasing resource
def destroy():
    GPIO.output(Rpin, GPIO.HIGH)
    GPIO.cleanup()

