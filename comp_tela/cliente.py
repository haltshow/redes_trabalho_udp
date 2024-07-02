import socket
import cv2
import numpy as np
import struct

# Endereço e porta do servidor
SERVER_ADDRESS = '26.210.161.25'
SERVER_PORT = 12345
HEADER_SIZE = struct.calcsize("I")  # Tamanho do cabeçalho para controle de fragmentação (4 bytes)

# Criação do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem para se registrar no servidor como viewer
client_socket.sendto(b"type:viewer", (SERVER_ADDRESS, SERVER_PORT))

print("Registrado como viewer no servidor. Aguardando stream de vídeo...")

# Cria uma janela para mostrar o stream
cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)

buffer = bytearray()
expected_offset = 0
frame_size = None

try:
    while True:
        # Recebe os frames do vídeo
        fragment, _ = client_socket.recvfrom(65507)
        if len(fragment) > HEADER_SIZE:
            offset = struct.unpack("I", fragment[:HEADER_SIZE])[0]
            if offset == expected_offset:
                buffer.extend(fragment[HEADER_SIZE:])
                expected_offset += len(fragment) - HEADER_SIZE

            # Detecta o fim de um frame baseado no tamanho do datagrama recebido
            if len(fragment) < 65507:
                if buffer:
                    np_data = np.frombuffer(buffer, dtype=np.uint8)
                    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
                    if frame is not None:
                        if frame_size is None:
                            frame_size = (frame.shape[1], frame.shape[0])
                        frame = cv2.resize(frame, frame_size)  # Ajusta o tamanho do frame conforme necessário
                        cv2.imshow("Video Stream", frame)
                        if cv2.waitKey(1) == 27:  # Pressione 'Esc' para sair
                            break
                    else:
                        print("Frame vazio ou corrompido recebido.")
                    buffer = bytearray()
                    expected_offset = 0
                else:
                    print("Buffer vazio recebido no final do fragmento.")

except KeyboardInterrupt:
    print("\nCliente encerrado.")
finally:
    client_socket.close()
    cv2.destroyAllWindows()