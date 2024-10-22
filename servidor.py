import socket

# Configurações do servidor
HOST = '0.0.0.0'  # Escutar em todas as interfaces disponíveis
PORT = 12345       # Porta que o servidor vai escutar

# Criar um socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f'Servidor UDP escutando em {HOST}:{PORT}')

    while True:
        # Receber dados do cliente
        data, addr = server_socket.recvfrom(1024)  # Buffer de 1024 bytes
        print(f'Recebido: {data.decode()} de {addr}')

        # Enviar uma resposta de volta ao cliente
        response = 'Dados recebidos!'
        server_socket.sendto(response.encode(), addr)
