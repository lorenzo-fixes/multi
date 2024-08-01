import socket
import pickle
import threading

# Constants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
MAX_PLAYERS = 2

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print("Server started. Waiting for connections...")

players = []

def handle_client(conn, player_id):
    global players
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"Player {player_id} disconnected")
                players[player_id] = None
                break
            # Handle player input or game state updates
            # Example: Parse data, update game state, and broadcast to other players
            # Example: player_input = pickle.loads(data)
            # Example: broadcast(player_id, player_input)
        except:
            continue

def broadcast(player_id, data):
    global players
    for id, conn in enumerate(players):
        if id != player_id and conn:
            try:
                conn.send(pickle.dumps(data))
            except:
                continue

# Accept connections from clients
while len(players) < MAX_PLAYERS:
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")
    players.append(conn)
    player_id = len(players) - 1
    # Start a new thread to handle each client
    thread = threading.Thread(target=handle_client, args=(conn, player_id))
    thread.start()
