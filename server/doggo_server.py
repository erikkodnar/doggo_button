import socket
import threading
import sys
import base64

# import required module
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

def decode_base64(encoded_bytes: bytes) -> str:
    # Decode the Base64 encoded bytes
    decoded_bytes = base64.b64decode(encoded_bytes)
    # Convert the bytes to a string
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def start_server(host='localhost', port=5000):
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
        # Break the loop if the socket is closed to prevent sending on a closed socket
        print("Socket has been closed, shutting down the server.")
    finally:
        server_socket.close()
        print("Server has been shut down.")

def speak(id: int):
    if id in sound_id_map:
        sound_file = sound_id_map[id]
        # for playing mp3 file
        sound = AudioSegment.from_mp3(sound_file)
        print('playing sound using pydub')
        play(sound)
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
                # Speak the received message in a separate thread
                threading.Thread(target=speak, args=(int(decoded_data),), daemon=True).start()
                response = base64.b64encode(f'ACK: {decoded_data}'.encode('utf-8'))

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
    start_server()
