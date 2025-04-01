 # imports for flask server
from flask import Flask
from flask_cors import CORS
from flask import jsonify

# imports for components
import RPi.GPIO as GPIO
from time import sleep

RELAY_PIN = 23

# do this only ONCE when the application starts
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup(RELAY_PIN, GPIO.OUT)

# start with locked
relay_state = GPIO.LOW
GPIO.output(RELAY_PIN, relay_state) 

# flask setup
app = Flask(__name__)
CORS(app, supports_credentials=True)

# endpoints
@app.route("/togglelock")
def toggle_lock_endpoint():
    try:
        global relay_state 

        # toggle state
        if relay_state == GPIO.LOW:
            relay_state = GPIO.HIGH
            print("setting relay to 1")
        else:
            relay_state = GPIO.LOW
            print("setting relay 0")
        GPIO.output(RELAY_PIN, relay_state)

        # return the current state
        current_state_int = 1 if relay_state == GPIO.HIGH else 0

        return jsonify({"success": True, "relay_state": current_state_int})
    except:
        return jsonify({"success": False, "relay_state": 0})

@app.route("/nfc")
def nfc_endpoint():

    result = True
    return jsonify({"success": result})

@app.route("/fingerprint")
def fingerprint_endpoint():

    result = True
    return jsonify({"success": result})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True, port=5000)
    finally:
        # clean up GPIO when the server stops
        print("\ncleaning up GPIO...")

        GPIO.cleanup() 
