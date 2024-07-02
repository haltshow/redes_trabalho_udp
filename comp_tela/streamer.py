import socket
import cv2
import numpy as np
import pyautogui

# Endereço e porta do servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Tamanho máximo do datagrama
MAX_DATAGRAM_SIZE = 65507

# Criação do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem para se registrar no servidor como streamer
client_socket.sendto(b"type:streamer", (SERVER_ADDRESS, SERVER_PORT))

def capture_screen():
    # Captura a tela inteira
    screen = pyautogui.screenshot()
    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Corrige a conversão de cor
    return frame

def send_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  # Ajustar qualidade para equilibrar qualidade e tamanho
    frame_data = buffer.tobytes()
    print(f"Sending frame of size: {len(frame_data)}")

    # Segmentação e envio do frame em partes, se necessário
    for i in range(0, len(frame_data), MAX_DATAGRAM_SIZE):
        segment = frame_data[i:i+MAX_DATAGRAM_SIZE]
        client_socket.sendto(segment, (SERVER_ADDRESS, SERVER_PORT))
        print(f"Sent segment from {i} to {i + len(segment)}")

try:
    while True:
        screen_frame = capture_screen()
        send_frame(screen_frame)
        cv2.waitKey(40)  # Ajuste para cerca de 25 frames por segundo
except KeyboardInterrupt:
    print("\nStreaming interrompido.")
finally:
    client_socket.close()