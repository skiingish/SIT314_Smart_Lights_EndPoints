#!/bin/sh
# LightSwitchLauncher.sh
# Navigate to user pi's desktop and then start all the light switch python programs.

cd /
cd home/pi/Desktop/Switches
python3.7 lightswitchMQTT_testswitch001.py & python3.7 lightswitchMQTT_testswitch002.py && pg