from scapy.all import *
import struct
import random

# Definições de IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.172.164'  # IP de origem do cliente

# Função para criar uma mensagem de requisição
def create_request(tipo, identificador):
    request_byte_0 = (0 << 4) | (tipo & 0x0F)  # req/res é 0, tipo é passado na função
    request_byte_1 = (identificador >> 8) & 0xFF  # Parte alta do identificador
    request_byte_2 = identificador & 0xFF  # Parte baixa do identificador
    return bytes([request_byte_0, request_byte_1, request_byte_2])

# Função para calcular o checksum UDP com wraparound
def calculate_udp_checksum(src_ip, dst_ip, udp_header, udp_payload):
    # Cabeçalho Pseudo
    pseudo_header = (
        bytes([src_ip[0], src_ip[1], src_ip[2], src_ip[3]]) + 
        bytes([dst_ip[0], dst_ip[1], dst_ip[2], dst_ip[3]]) +
        bytes([0, 17]) +  # 0 e 17 (número do protocolo UDP)
        (len(udp_header) + len(udp_payload)).to_bytes(2, 'big')  # Comprimento do segmento UDP
    )
    
    # Dados para o checksum
    checksum_data = pseudo_header + udp_header + udp_payload

    # Ajusta para 16 bits
    total = 0
    for i in range(0, len(checksum_data), 2):
        if i + 1 < len(checksum_data):
            word = (checksum_data[i] << 8) + checksum_data[i + 1]
        else:
            word = (checksum_data[i] << 8)  # Se for ímpar, adiciona byte zero
        total += word
        # Wraparound
        total = (total & 0xFFFF) + (total >> 16)

    # Complemento de 1-bit
    checksum = ~total & 0xFFFF
    return checksum

# Função para enviar requisição e receber resposta
def send_request_and_receive_response(tipo):
    identificador = 23777  # Usando o identificador fornecido
    request = create_request(tipo, identificador)

    # Definindo portas e comprimento
    source_port = 59155
    destination_port = SERVER_PORT
    length = 8 + len(request)  # 8 bytes do cabeçalho + tamanho do payload

    # Criando o cabeçalho UDP
    udp_header = struct.pack('!HHHH', source_port, destination_port, length, 0)  # Checksum inicial é 0

    # Calculando o checksum
    src_ip = list(map(int, SOURCE_IP.split('.')))
    dst_ip = list(map(int, SERVER_IP.split('.')))
    checksum = calculate_udp_checksum(src_ip, dst_ip, udp_header, request)

    # Atualizando o cabeçalho UDP com o checksum calculado
    udp_header = struct.pack('!HHHH', source_port, destination_port, length, checksum)

    # Criando o pacote UDP
    udp_packet = IP(src=SOURCE_IP, dst=SERVER_IP) / UDP(sport=source_port, dport=destination_port) / request

    # Enviando o pacote
    send(udp_packet)

    print(f"Requisição enviada: Tipo {tipo}, Identificador {identificador}")

    # Espera por uma resposta
    response = sniff(filter=f"udp and src host {SERVER_IP} and src port {SERVER_PORT}", count=1, timeout=15)

    if response:
        response_packet = response[0]
        print(f"Resposta recebida (hex): {response_packet[UDP].payload.load.hex()}")

        # Extrai os campos da resposta
        resposta = response_packet[UDP].payload.load
        tipo_resposta = (resposta[0] >> 4) & 0x0F  # 4 bits de req/res
        identificador_resposta = (resposta[1] << 8) | resposta[2]
        tamanho_resposta = resposta[3]

        try:
            resposta_texto = resposta[4:4 + tamanho_resposta].decode('ascii')
        except UnicodeDecodeError:
            resposta_texto = "<Ops, erro de decodificação>"

        print(f"Tipo de resposta: {tipo_resposta}")
        print(f"Identificador de resposta: {identificador_resposta}")
        print(f"Tamanho da resposta: {tamanho_resposta}")
        print(f"Resposta propriamente dita: {resposta_texto}")
    else:
        print("Tempo esgotado. Nenhuma resposta recebida do servidor.")

# Teste da função
send_request_and_receive_response(0)