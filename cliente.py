import socket

def cliente_udp(server_ip, port):
    # Cria um socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Mensagem a ser enviada
    message = "Olá do cliente!"
    
    # Envia a mensagem ao servidor
    client_socket.sendto(message, (server_ip, port))
    print(f'Mensagem enviada para {server_ip}:{port}')

    # Recebe resposta do servidor
    data, addr = client_socket.recvfrom(1024)
    print(f'Resposta recebida: {data} de {addr}')

if __name__ == '__main__':
    servidor_ip = '187.64.55.75'  # Substitua pelo IP público do servidor
    cliente_udp(servidor_ip, 12345)  # Use a mesma porta do servidor
