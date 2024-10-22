import socket

# Configurações do cliente
SERVER_IP = '177.37.173.165'  # IP do servidor (substitua pelo IP correto)
SERVER_PORT = 12345          # Porta do servidor

# Criar um socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    message = 'Olá, servidor!'
    
    # Enviar dados ao servidor
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    
    # Receber resposta do servidor
    data, addr = client_socket.recvfrom(1024)  # Buffer de 1024 bytes
    print(f'Resposta do servidor: {data.decode()}')
