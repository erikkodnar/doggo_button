import os
import socket
import threading
import sys
import base64
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from pydub.playback import play

sound_id_map = {
    1: 'assets/snuggles.mp3',
    2: 'assets/play.mp3',
    3: 'assets/pee.mp3',
    4: 'assets/mom.mp3',
    5: 'assets/JessieJane.mp3',
    6: 'assets/dad.mp3',
}

# Preload sound files into a dictionary
preloaded_sounds = {}

def preload_sounds():
    for id, file_path in sound_id_map.items():
        sound = AudioSegment.from_mp3(file_path)
        preloaded_sounds[id] = sound

def decode_base64(encoded_bytes: bytes) -> str:
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def start_server(host='192.168.4.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")

    # Start the thread for handling keyboard input in dev mode
    if '-dev' in sys.argv:
        threading.Thread(target=interactive_shell, args=(server_socket,), daemon=True).start()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected by {client_address}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    except OSError:
        print("Socket has been closed, shutting down the server.")
    finally:
        server_socket.close()
        print("Server has been shut down.")

def speak(id: int, created_at: str):
    if id in preloaded_sounds:
        sound = preloaded_sounds[id]
        created_at_time = datetime.fromisoformat(created_at)

        # Store the start time right before playing the sound
        start_time = datetime.now()
        print('playing sound using pydub')
        play(sound)
        end_time = datetime.now()

        # Calculate the delay
        delay = (start_time - created_at_time).total_seconds()
        print(f"Time difference between message created and sound starting: {delay} seconds")
    else:
        print(f"Unknown sound ID: {id}")

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            decoded_data = decode_base64(data)
            print(f"Received data: {decoded_data}")

            if decoded_data == 'ping':
                print("Ping received, sending pong...")
                response = base64.b64encode(b'pong')
            else:
                try:
                    message = json.loads(decoded_data)
                    message_id = int(message['id'])
                    created_at = message['created_at']
                    # Submit the speak task to the thread pool executor
                    executor.submit(speak, message_id, created_at)
                    response = base64.b64encode(f'ACK: {message_id}'.encode('utf-8'))
                except (ValueError, KeyError) as e:
                    print(f"Error parsing message: {e}")
                    response = base64.b64encode(b'ERROR')

            client_socket.sendall(response)
    finally:
        client_socket.close()
        print("Connection closed")

def interactive_shell(server_socket):
    while True:
        cmd = input("Enter 'q' to quit: ")
        if cmd == 'q':
            print("Shutting down the server...")
            server_socket.close()
            break

if __name__ == "__main__":
    preload_sounds()
    executor = ThreadPoolExecutor(max_workers=4)  # Initialize the thread pool executor with 4 workers

    # Start the access point services
    os.system("sudo systemctl unmask hostapd")
    os.system("sudo systemctl enable hostapd")
    os.system("sudo systemctl start hostapd")
    os.system("sudo systemctl start dnsmasq")
    
    # Add a delay to ensure the services have started
    time.sleep(10)  # Adjust the sleep time as necessary

    # Manually assign the IP address to wlan1
    os.system("sudo ip addr add 192.168.4.1/24 dev wlan1")
    os.system("sudo ip link set wlan1 up")
    
    start_server()
