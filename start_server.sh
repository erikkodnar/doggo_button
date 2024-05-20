#!/bin/bash

# Start the access point
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Navigate to the directory containing the Python script
cd /home/pi/doggo_button/server

# Start venv
source venv/bin/activate

# Start the Python server
python doggo_server.py -dev
