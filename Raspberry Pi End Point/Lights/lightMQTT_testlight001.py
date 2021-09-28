# Created by Sean Corcoran
# Light End Point.
# For SIT314 - Final Project - Deakin University - 2021

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

# Set up the output pin for the light
outputPin = 8 # pin to output high voltage (postive of the LED) <-- Change depending on the test light and where it's connected. 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(outputPin, GPIO.OUT, initial=GPIO.LOW)

# The unique device / light ID.
device_id = 'testlight001' # <-- Change this value when adding test lights.

# Holds the current light state.
light = 0

# When connected to the MQTT Broker service.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the all topic.
    client.subscribe("/scorlights/")
    # Subscribe to this device's topic.
    client.subscribe("/scorlights/+/+/" + device_id + "/")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    # Using the global stored light.
    global light
    print(f"{msg.topic} {msg.payload}")
    
    # Split up the message
    message = str(msg.payload).split("'")
    
    # If message is toggle.
    if (message[1] == "toggle"):
        if (light == 0):
            GPIO.output(outputPin, GPIO.HIGH)
            light = 1
        else:
            GPIO.output(outputPin, GPIO.LOW)
            light = 0
    
    # If message is stateChange. 
    # Turn on.
    if (message[1] == "on"):
        if (light == 0):
            GPIO.output(outputPin, GPIO.HIGH)
            light = 1
    # Turn off.
    if (message[1] == "off"):
        if (light == 1):
            GPIO.output(outputPin, GPIO.LOW)
            light = 0

# Report the light state back to the backend. (if needed)
def reportState():
    #Send the current light
    print("Current light state: " + light)

# Connect to the MQTT client.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.hivemq.com", 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()