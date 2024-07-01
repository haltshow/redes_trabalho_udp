import socket
import cv2
import numpy as np
import pyautogui
import threading

# Endereço e porta do servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Tamanho máximo do datagrama (de acordo com a documentação do Python para sistemas modernos)
MAX_DATAGRAM_SIZE = 65507

# Criação do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem vazia para se registrar no servidor
client_socket.sendto(b'', (SERVER_ADDRESS, SERVER_PORT))

print("Conectado ao servidor. Transmitindo e recebendo tela...")

def capture_and_send_screen():
    while True:
        # Captura a tela
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        # Envia o frame capturado para o servidor
        client_socket.sendto(frame_data, (SERVER_ADDRESS, SERVER_PORT))

def receive_and_display_screen():
    try:
        while True:
            frame_data, _ = client_socket.recvfrom(MAX_DATAGRAM_SIZE)
            np_data = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow('Screen Stream', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'Esc' para sair
                break
    except KeyboardInterrupt:
        print("\nCliente encerrado.")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()

# Inicia as threads para capturar/ enviar e receber/exibir a tela
send_thread = threading.Thread(target=capture_and_send_screen)
receive_thread = threading.Thread(target=receive_and_display_screen)

send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()
