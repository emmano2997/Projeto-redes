import socket
import struct
import random

# Definições de IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.173.165' # IP de origem do cliente

# Função para criar uma mensagem de requisição
def create_request(tipo, identificador):
    request_byte_0 = (0 << 4) | (tipo & 0x0F)  # req/res é 0, tipo é passado na função
    request_byte_1 = (identificador >> 8) & 0xFF  # Parte alta do identificador
    request_byte_2 = identificador & 0xFF  # Parte baixa do identificador
    return bytes([request_byte_0, request_byte_1, request_byte_2])

# Função para calcular o checksum (para o cabeçalho UDP)
def calculate_checksum(header):
    total = 0
    for i in range(0, len(header), 2):
        total += (header[i] << 8) + (header[i + 1])
    while (total >> 16):
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF

# Função para criar o cabeçalho UDP
def create_udp_header(src_port, dest_port, length, checksum):
    return struct.pack('!HHHH', src_port, dest_port, length, checksum)

# Função para enviar requisição e receber resposta
def send_request_and_receive_response(tipo):
    identificador = random.randint(1, 65535)  # Identificador aleatório entre 1 e 65535
    request = create_request(tipo, identificador)

    # Cabeçalho UDP
    src_port = random.randint(1024, 65535)  # Porta de origem aleatória
    dest_port = SERVER_PORT                   # Porta de destino
    length = 8 + len(request)                 # Comprimento do cabeçalho UDP + payload
    checksum = 0  # Inicialmente 0, será recalculado

    # Cria o cabeçalho UDP
    udp_header = create_udp_header(src_port, dest_port, length, checksum)

    # Pseudo-cabeçalho para calcular o checksum
    src_ip = socket.inet_aton(SOURCE_IP)
    dest_ip = socket.inet_aton(SERVER_IP)
    zero = 0
    protocol = 17  # 17 para UDP
    pseudo_header = struct.pack('!4s4sBBH', src_ip, dest_ip, zero, protocol, length)

    # Calcula o checksum
    checksum = calculate_checksum(pseudo_header + udp_header + request)

    # Cria o cabeçalho UDP final com o checksum correto
    udp_header = create_udp_header(src_port, dest_port, length, checksum)

    # Combina o cabeçalho UDP e o payload
    packet = udp_header + request

    # Cria o socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)  # Timeout de 5 segundos
        # Envia a requisição para o servidor
        sock.sendto(packet, (SERVER_IP, SERVER_PORT))
        print(f"Requisição enviada: Tipo {tipo}, Identificador {identificador}")

        try:
            # Recebe a resposta do servidor
            response, _ = sock.recvfrom(1024)  # Tamanho máximo da resposta: 1024 bytes
            print(f"Resposta recebida (hex): {response.hex()}")

            # Extrai os campos da resposta
            tipo_resposta = (response[0] >> 4) & 0x0F  # 4 bits de req/res
            identificador_resposta = (response[1] << 8) | response[2]
            tamanho_resposta = response[3]
            resposta_texto = response[4:4+tamanho_resposta].decode('ascii')

            print(f"Tipo de resposta: {tipo_resposta}")
            print(f"Identificador de resposta: {identificador_resposta}")
            print(f"Tamanho da resposta: {tamanho_resposta}")
            print(f"Resposta propriamente dita: {resposta_texto}")

        except socket.timeout:
            print("Tempo esgotado. Nenhuma resposta recebida do servidor.")

while True:
    print("Escolha o tipo de requisição:")
    print("1. Data e hora atual")
    print("2. Mensagem motivacional para o fim do semestre")
    print("3. Quantidade de respostas emitidas pelo servidor")
    print("4. Sair")
    
    opcao = input("Digite a sua escolha: ")

    if opcao == '1':
        send_request_and_receive_response(0)
    elif opcao == '2':
        send_request_and_receive_response(1)
    elif opcao == '3':
        send_request_and_receive_response(2)
    elif opcao == '4':
        print("Saindo...")
        break
    else:
        print("Opção inválida, tente novamente.")
