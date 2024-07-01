import socket

# Endereço e porta do servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Criação do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem vazia para se registrar no servidor
client_socket.sendto(b'', (SERVER_ADDRESS, SERVER_PORT))

print("Conectado ao servidor. Aguardando notificações...")

try:
    while True:
        # Recebe a notificação do servidor
        response, _ = client_socket.recvfrom(1024)
        print(f"Notificação recebida: {response.decode()}")

except KeyboardInterrupt:
    print("\nCliente encerrado.")
finally:
    client_socket.close()