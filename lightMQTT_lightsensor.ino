// Created by Sean Corcoran
// Light Meter Switch
// For SIT314 - Final Project - Deakin University - 2021

// Include MQTT.
#include <MQTT.h>
#include "application.h"

// Pin to read light sensor values.
int luxSensor = A0;

// Light reading. 
int luxValue;

// The current switch state.
int state = 0; 

// The unique device ID
String device_id = "lightsensor001";

// Define the client. (including the address)
MQTT client("broker.hivemq.com", 1883, callback);

// Recieve message (This can be blank as we are not recieving any messages)
void callback(char* topic, byte* payload, unsigned int length) {
}

// Upon Boot.
void setup() {
    // Set the light sensor pin as input.
    pinMode(luxSensor, INPUT);

    // Connect to the server(unique id by Time.now())
    client.connect("sparkclient_" + String(Time.now()));

    // Publish a online message.
    if (client.isConnected()) {
        client.publish("/scorlights/message/", device_id + " : Online");
    }
}

// The main loop.
void loop() {
    // If connected to client.
    if (client.isConnected())

    // Get the reading from the light sensor.
    luxValue = analogRead(luxSensor);
    
    // If the reading is below 20 lux and the current state is off then issue a on command, else turn the lights off.
    if (luxValue < 20 && state == 0)
    {
        // Change the state to on.
        state = 1;
        
        // Publish the message to MQTT
        client.publish("/scorlights/switch/" + device_id + "/","on");
        
        // Output to the Particle console for debugging.
        Particle.publish("luxValue", String(luxValue));
        Particle.publish("state", String(state));
        
        // Wait before taking another reading. 
        delay(10000);
    }
    // If the reading is above or equal to 20 and the current state is on, then issue a off command.
    if (luxValue >= 20 && state == 1)
    {
        // Change the state to off.
        state = 0;
        
        // Publish the message to MQTT
        client.publish("/scorlights/switch/" + device_id + "/","off");
        
        // Output to the Particle console for debugging.
        Particle.publish("luxValue", String(luxValue));
        Particle.publish("state", String(state));
        
        // Wait before taking another reading.
        delay(10000);
    }

    // Keep the client online. 
    client.loop();
}
