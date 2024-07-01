import socket
import threading
import cv2
import numpy as np

# Endereço e porta do servidor
SERVER_ADDRESS = '26.210.161.25'
SERVER_PORT = 12345

# Caminho do vídeo a ser transmitido
VIDEO_PATH = 'video.mp4'

# Tamanho máximo do datagrama
MAX_DATAGRAM_SIZE = 65507

# Criação do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

clients = set()

# Função para transmitir o vídeo
def stream_video():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            print("Reiniciando o vídeo...")
            cap = cv2.VideoCapture(VIDEO_PATH)
            continue
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        for client in clients:
            server_socket.sendto(frame_data, client)
        
        cv2.waitKey(33)  # Aproximadamente 30 fps

# Função para receber mensagens dos clientes
def receive_clients():
    while True:
        message, client_address = server_socket.recvfrom(1024)
        if client_address not in clients:
            print(f"Novo cliente conectado: {client_address}")
            clients.add(client_address)

# Thread para receber clientes
client_thread = threading.Thread(target=receive_clients)
client_thread.start()

print("Servidor iniciado e aguardando conexões...")

# Inicia o streaming de vídeo
stream_video()