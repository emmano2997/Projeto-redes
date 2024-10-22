import socket

def servidor_udp(port):
    # Cria um socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Associa o socket a um endereço e porta
    server_socket.bind(('', port))
    print(f'Servidor UDP ouvindo na porta {port}')

    while True:
        # Recebe dados do cliente
        data, addr = server_socket.recvfrom(1024)
        print(f'Recebido {data} de {addr}')
        
        # Envia uma resposta ao cliente
        response = 'Olá do servidor!'
        server_socket.sendto(response, addr)

if __name__ == '__main__':
    servidor_udp(12345)  # Substitua 12345 pela porta desejada
