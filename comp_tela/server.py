import socket
import cv2
import numpy as np
import struct

# Configuração do servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345
MAX_DATAGRAM_SIZE = 65507
HEADER_SIZE = struct.calcsize("I")  # Tamanho do cabeçalho para controle de fragmentação (4 bytes)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

clients = {}
streamer_address = None

def fragment_frame(frame_data):
    fragments = []
    for i in range(0, len(frame_data), MAX_DATAGRAM_SIZE - HEADER_SIZE):
        header = struct.pack("I", i)  # Header indicando o offset do fragmento
        fragment = header + frame_data[i:i + (MAX_DATAGRAM_SIZE - HEADER_SIZE)]
        fragments.append(fragment)
    return fragments

def redistribute_frame(frame_data):
    fragments = fragment_frame(frame_data)
    for client_address in clients:
        if client_address != streamer_address:
            for fragment in fragments:
                server_socket.sendto(fragment, client_address)

def handle_client(client_address, frame_buffer):
    global streamer_address
    if client_address == streamer_address:
        np_data = np.frombuffer(frame_buffer, dtype=np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            redistribute_frame(buffer.tobytes())
        else:
            print("Erro ao decodificar o frame.")
        clients[client_address] = bytearray()

def receive_data():
    global streamer_address
    while True:
        data, addr = server_socket.recvfrom(MAX_DATAGRAM_SIZE)
        if addr not in clients:
            clients[addr] = bytearray()
            if data.startswith(b"type:"):
                if b"streamer" in data:
                    streamer_address = addr
                    print("Streamer registrado:", addr)
                elif b"viewer" in data:
                    print("Viewer registrado:", addr)
                continue

        clients[addr].extend(data)
        if len(data) < MAX_DATAGRAM_SIZE:
            handle_client(addr, clients[addr])

print("Servidor iniciado e aguardando conexões...")
receive_data()