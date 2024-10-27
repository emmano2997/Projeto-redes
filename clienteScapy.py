from scapy.all import IP, UDP, send, Raw
import random
import struct

# definindo as portas
org_port = 12345   # porta de origem
dest_port = 50000   # porta de destino
#payload = b'\x02\x5C\xE1'  # payload de 3 bytes
# 0x025CE1 (req da quant de respostas enviadas pelo server, com id 23777)

# Função para criar uma mensagem de requisição
def create_request(tipo, identificador):
    request_byte_0 = (0 << 4) | (tipo & 0x0F)  # req/res é 0, tipo é passado na função
    request_byte_1 = (identificador >> 8) & 0xFF  # Parte alta do identificador
    request_byte_2 = identificador & 0xFF  # Parte baixa do identificador
    return bytes([request_byte_0, request_byte_1, request_byte_2])

# Função para enviar requisição e receber resposta
def send_request_and_receive_response(tipo):
    identificador = random.randint(1, 65535)  # Identificador aleatório entre 1 e 65535
    request_payload = create_request(tipo, identificador)


    # cabeçalho IP
    ip_header = IP(src = '177.37.172.164', dst = '15.228.191.109')

    # cabeçalho UDP
    udp_header = UDP(sport = org_port, dport = dest_port, len = 8 + len(request_payload), chksum=0)
    # porta de origem, porta de destino, comprimento do segmento (8 + 3 de payload), checksum que inicia 0

    # pacote
    packet = ip_header / udp_header / Raw(load = request_payload)# '/' -> concatenação de camadas do pacotes

    
    print("Pacote: ")
    packet.show()



# Função para calcular o checksum UDP com wraparound
def calculate_udp_checksum(src_ip, dst_ip, udp_header, udp_payload):
    # Cabeçalho Pseudo
    # Converte IPs de origem e destino em bytes
    pseudo_header = (
        bytes([src_ip[0], src_ip[1], src_ip[2], src_ip[3]]) + 
        bytes([dst_ip[0], dst_ip[1], dst_ip[2], dst_ip[3]]) +
        bytes([0, 17]) +  # 0 e 17 (número do protocolo UDP)
        (len(udp_header) + len(udp_payload)).to_bytes(2, 'big')  # Comprimento do segmento UDP
    )
    
    # Dados para o checksum
    checksum_data = pseudo_header + udp_header.build() + udp_payload

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