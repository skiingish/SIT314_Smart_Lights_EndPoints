# Created by Sean Corcoran
# Light On Off Switch End Point.
# For SIT314 - Final Project - Deakin University - 2021

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

# The unique device / Switch ID.
device_id = 'testswitch002'

# Inputpins
inputOffPin = 35
inputOnPin = 37

# Holds the current switch state.
state = 0

# Display when connected.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(inputOffPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin to be an input pin and set initial value to be pulled low (off)
GPIO.setup(inputOnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin to be an input pin and set initial value to be pulled low (off)


while True: # Run forever
    # If there was input on the ON pin and the light is currently off, turn the light on.
    if GPIO.input(inputOnPin) == GPIO.HIGH and state == 0:
        # Change the switch state to on.
        state = 1

        # Connect to the client.
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("broker.hivemq.com", 1883, 60)

        # The four parameters are topic (in this case as a switch with the device id), sending content (this is a toggle switch), QoS and whether retaining the message respectively
        client.publish('/scorlights/switch/' + device_id + "/", payload='on', qos=0, retain=False)
        print("send ON to /scorlights/switch/" + device_id +"/")
    
    # If there was input on the OFF pin and the light is currently on, turn the light off.
    if GPIO.input(inputOffPin) == GPIO.HIGH and state == 1:
        # Change the switch state to on.
        state = 0

        # Connect to the client.
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("broker.hivemq.com", 1883, 60)

        # The four parameters are topic (in this case as a switch with the device id), sending content (this is a toggle switch), QoS and whether retaining the message respectively
        client.publish('/scorlights/switch/' + device_id + "/", payload='off', qos=0, retain=False)
        print("send OFF to /scorlights/switch/" + device_id +"/")
