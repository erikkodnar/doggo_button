import socket
import base64
import threading
import time
import json
from datetime import datetime

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.lock = threading.Lock()
        self.connected = False
        self.connect()

    def connect(self):
        with self.lock:
            if self.client_socket:
                self.client_socket.close()
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            attempts = 0
            while attempts < 5:
                try:
                    self.client_socket.connect(('192.168.4.1', 5000))
                    self.connected = True
                    print("Connected to the server.")
                    return
                except socket.error as e:
                    print(f"Attempt {attempts + 1} failed: {e}")
                    time.sleep(2)  # wait for 2 seconds before retrying
                    attempts += 1
            self.connected = False
            print("Failed to connect to the server after several attempts.")

    def send_ping(self):
        while True:
            if not self.connected:
                print("Not connected to server. Attempting to reconnect...")
                self.connect()
                if not self.connected:
                    continue  # skip this ping cycle if still not connected
            try:
                print("Sending ping...")
                self.client_socket.sendall(base64.b64encode(b'ping'))
                response = self.client_socket.recv(1024)
                if base64.b64decode(response).decode('utf-8') != 'pong':
                    print("No pong received, restarting connection.")
                    self.connected = False
            except socket.error as e:
                print(f"Error during communication: {e}")
                self.connected = False
            time.sleep(5)

    def send_message(self):
        try:
            while True:
                message = input("Enter your message (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    break

                if not self.connected:
                    print("Not connected to server.")
                    continue

                message_id = message  # In this example, using the input message as the ID
                created_at = datetime.now().isoformat()
                message_dict = {
                    "id": message_id,
                    "created_at": created_at
                }

                json_message = json.dumps(message_dict)
                base64_message = base64.b64encode(json_message.encode('utf-8'))
                self.client_socket.sendall(base64_message)

                response = self.client_socket.recv(1024)
                print('Received from server:', base64.b64decode(response).decode('utf-8'))

        finally:
            self.connected = False
            self.client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    client = Client('localhost', 5000)
    threading.Thread(target=client.send_ping, daemon=True).start()
    client.send_message()
