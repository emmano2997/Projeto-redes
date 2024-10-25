from scapy.all import IP, UDP, send, Raw
import struct
import socket

def build_udp_header(org_port, dest_port, udp_payload):
    # Definindo tamanho total do UDP (cabeçalho + payload)
    udp_length = 8 + len(udp_payload)

    # Checksum inicial (será calculado depois)
    checksum = 0

    # Criando cabeçalho UDP sem o checksum (será adicionado depois)
    udp_header = struct.pack('!4H', org_port, dest_port, udp_length, checksum)

    return udp_header

def calculate_udp_checksum(org_ip, dest_ip, udp_header, udp_payload):
    # Construindo o pseudo-cabeçalho IP para o cálculo do checksum
    pseudo_header = struct.pack(
        '!4s4sBBH', 
        socket.inet_aton(org_ip),            # Endereço IP de origem
        socket.inet_aton(dest_ip),           # Endereço IP de destino
        0,                                   # Campo reservado
        socket.IPPROTO_UDP,                  # Protocolo (UDP = 17)
        len(udp_header) + len(udp_payload)   # Comprimento total do UDP (cabeçalho + payload)
    )
    
    # Concatenando pseudo-cabeçalho, cabeçalho UDP e payload para o cálculo
    checksum_data = pseudo_header + udp_header + udp_payload
    checksum = 0
    
    # Somando conjuntos de 2 bytes
    for i in range(0, len(checksum_data), 2):
        word = (checksum_data[i] << 8) + (checksum_data[i + 1])
        checksum += word
        checksum = (checksum >> 16) + (checksum & 0xFFFF) #wraparound

    checksum = ~checksum & 0xFFFF  # Complemento de 1 para checksum
    return checksum

def send_udp_packet(org_ip, dest_ip, org_port, dest_port, payload):
    # Construindo o cabeçalho UDP
    udp_payload = payload.encode()
    udp_header = build_udp_header(org_port, dest_port, udp_payload)

    # Calculando o checksum UDP
    checksum = calculate_udp_checksum(org_ip, dest_ip, udp_header, udp_payload)

    # Atualizando o checksum no cabeçalho UDP
    udp_header = struct.pack('!4H', org_port, dest_port, 8 + len(udp_payload), checksum)

    # Criando o pacote IP/UDP com Scapy e adicionando manualmente o cabeçalho UDP
    packet = IP(src=org_ip, dst=dest_ip) / Raw(load=udp_header + udp_payload)

    # Enviando o pacote usando Scapy
    send(packet)

if __name__ == '__main__':
    
    org_ip = '127.0.0.1' #ip do cliente
    dest_ip = '15.228.191.109'
    org_port = 12345
    dest_port = 50000
    payload = "Hello, World!"

    send_udp_packet(org_ip, dest_ip, org_port, dest_port, payload)
