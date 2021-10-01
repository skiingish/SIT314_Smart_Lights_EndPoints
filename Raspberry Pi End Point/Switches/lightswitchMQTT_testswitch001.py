# Created by Sean Corcoran
# Light Toggle Switch End Point.
# For SIT314 - Final Project - Deakin University - 2021

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

# # The unique device / Switch ID.
device_id = 'testswitch'

# This is a toggle switch
message = 'toggle'

# Inputpin
inputPin = 10;

# Display when connected.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

GPIO.setwarnings(False) # Ignore warning for now

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    # If there was input.
    if GPIO.input(inputPin) == GPIO.HIGH:
        print("Button was pushed!")
        print("------")
        
        # Connect to the client.
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("broker.hivemq.com", 1883, 60)

        # The four parameters are topic (in this case as a switch with the device id), sending content (this is a toggle switch), QoS and whether retaining the message respectively
        client.publish('/scorlights/switch/' + device_id + "/", payload=message, qos=0, retain=False)
        print(f"send {message} to /scorlights/switch/" + device_id + "/")
        
        # Sleep for 2 seconds as not to flood messages.
        time.sleep(2)
