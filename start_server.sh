#!/bin/bash

# Start the access point
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Navigate to the directory containing the Python script
cd /home/pi/doggo_button/server

# Start the Python server
python3 doggo_server.py -dev
