import struct
import socket
from scapy.all import *

# Informações de IP e portas do cliente e servidor
CLIENT_IP = 'seu_IP_cliente_aqui'
SERVER_IP = '15.228.191.109'
CLIENT_PORT = 59155  # Porta de origem
SERVER_PORT = 50000  # Porta de destino

# Função para calcular o checksum manualmente
def udp_checksum(ip_src, ip_dst, udp_len, udp_header, payload):
    # Pseudo-cabeçalho para o cálculo do checksum
    pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(ip_src), socket.inet_aton(ip_dst), 0, socket.IPPROTO_UDP, udp_len)
    
    # Adiciona o pseudo-header ao cabeçalho UDP e payload
    checksum_data = pseudo_header + udp_header + payload

    # Se o número de bytes for ímpar, adiciona um byte de padding
    if len(checksum_data) % 2 != 0:
        checksum_data += b'\x00'

    # Soma todos os pares de bytes
    checksum = 0
    for i in range(0, len(checksum_data), 2):
        word = (checksum_data[i] << 8) + checksum_data[i + 1]
        checksum += word
    
    # Soma overflow (carry)
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += (checksum >> 16)

    # Inverte os bits (complemento de 1)
    checksum = ~checksum & 0xFFFF
    return checksum

# Função para criar uma mensagem de requisição
def create_request(tipo, identificador):
    # Formato da mensagem: 4 bits req/res (0 para requisição), 4 bits tipo, e 2 bytes identificador
    request_byte_0 = (0 << 4) | (tipo & 0x0F)  # req/res é 0, tipo é passado na função
    request_byte_1 = (identificador >> 8) & 0xFF  # Parte alta do identificador
    request_byte_2 = identificador & 0xFF  # Parte baixa do identificador
    return bytes([request_byte_0, request_byte_1, request_byte_2])

# Função para enviar requisição com UDP e checksum dinâmico
def send_udp_request(tipo):
    identificador = random.randint(1, 65535)  # Identificador aleatório entre 1 e 65535
    request_data = create_request(tipo, identificador)

    # Calcula o comprimento do segmento UDP (cabeçalho + payload)
    udp_length = 8 + len(request_data)  # Cabeçalho UDP tem 8 bytes
    
    # Constrói o cabeçalho UDP sem o checksum (coloca provisoriamente 0x0000)
    udp_header = struct.pack('!HHHH', CLIENT_PORT, SERVER_PORT, udp_length, 0x0000)
    
    # Calcula o checksum UDP
    checksum = udp_checksum(CLIENT_IP, SERVER_IP, udp_length, udp_header, request_data)
    
    # Constrói o cabeçalho UDP final com o checksum calculado
    udp_header = struct.pack('!HHHH', CLIENT_PORT, SERVER_PORT, udp_length, checksum)

    # Constrói o pacote completo IP + UDP + Payload
    ip_header = IP(src=CLIENT_IP, dst=SERVER_IP)
    packet = ip_header / udp_header / request_data
    
    # Envia o pacote
    send(packet)
    print(f"Requisição enviada: Tipo {tipo}, Identificador {identificador}, Checksum {hex(checksum)}")

send_udp_request(1)  
