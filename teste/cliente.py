import socket
import cv2
import numpy as np

# Endereço e porta do servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Criação do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem vazia para se registrar no servidor
client_socket.sendto(b'', (SERVER_ADDRESS, SERVER_PORT))

print("Conectado ao servidor. Aguardando stream de vídeo...")

try:
    while True:
        frame_data, _ = client_socket.recvfrom(65536)  # Recebe os frames do vídeo
        np_data = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) == 27:  # Pressione 'Esc' para sair
            break

except KeyboardInterrupt:
    print("\nCliente encerrado.")
finally:
    client_socket.close()
    cv2.destroyAllWindows()