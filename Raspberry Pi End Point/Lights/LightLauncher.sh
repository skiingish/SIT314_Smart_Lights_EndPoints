#!/bin/sh
# LightLauncher.sh
# Navigate to user pi's desktop and then start all the light python programs.

cd /
cd home/pi/Desktop/Lights
python3.7 lightMQTT_testlight001.py & python3.7 lightMQTT_testlight002.py & python3.7 lightMQTT_testlight003.py & python3.7 lightMQTT_testlight004.py & python3.7 lightMQTT_testlight005.py & python3.7 lightMQTT_testlight006.py & python3.7 lightMQTT_testlight007.py && pg