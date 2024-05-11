#!/bin/bash
echo "---Setting up server---"
echo "Creating virtual environment"
cd server
python3 -m venv venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing dependencies"
pip install -r requirements.txt

echo "Run the application with 'cd server && venv/bin/activate && python doggo_server.py'"
deactivate
cd ..


echo "---Setting up test client---"
echo "Creating virtual environment"
cd test_client
python3 -m venv venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing dependencies"
pip install -r requirements.txt

echo "Run the test client application with 'cd test_client && venv/bin/activate && python main.py'"
deactivate
cd ..
