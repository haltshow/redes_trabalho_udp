import socket
import time

# Endereço e porta do servidor
SERVER_ADDRESS = '26.210.161.25'
SERVER_PORT = 12345

# Criação do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

clients = set()
message_interval = 1  # Intervalo de tempo em segundos entre as mensagens

print("Servidor UDP iniciado e aguardando conexões...")

try:
    while True:
        # Tenta receber dados (deve ser feito para registrar novos clientes)
        try:
            server_socket.settimeout(message_interval)
            message, client_address = server_socket.recvfrom(1024)
            print(f"Novo cliente conectado: {client_address}")
            clients.add(client_address)
        except socket.timeout:
            pass  # Timeout é esperado

        # Envia uma mensagem padrão para todos os clientes conectados
        for client in clients:
            server_socket.sendto("Mensagem padrão do servidor".encode('utf-8'), client)

except KeyboardInterrupt:
    print("\nServidor encerrado.")
finally:
    server_socket.close()