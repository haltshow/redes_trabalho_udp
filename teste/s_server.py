import socket
import threading

# Endereço e porta do servidor
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Tamanho máximo do datagrama (de acordo com a documentação do Python para sistemas modernos)
MAX_DATAGRAM_SIZE = 65507

# Criação do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

clients = set()

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

try:
    while True:
        # Recebe frames do cliente que transmite a tela
        frame_data, client_address = server_socket.recvfrom(MAX_DATAGRAM_SIZE)
        # Envia os frames para todos os outros clientes conectados
        for client in clients:
            if client != client_address:
                server_socket.sendto(frame_data, client)

except KeyboardInterrupt:
    print("\nServidor encerrado.")
finally:
    server_socket.close()
