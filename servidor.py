import socket

# Criar um socket UDP
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definir endereço e porta
endereco = ('0.0.0.0', 12345)  # Escutar em todas as interfaces na porta 12345
servidor_socket.bind(endereco)

print("Servidor UDP aguardando mensagens...")

while True:
    # Receber dados
    dados, cliente_endereco = servidor_socket.recvfrom(1024)  # Buffer de 1024 bytes
    print(f"Recebido de {cliente_endereco}: {dados.decode('utf-8')}")  # Decodificando de bytes para string
    
    # Responder ao cliente
    servidor_socket.sendto(b'Mensagem recebida!', cliente_endereco)
