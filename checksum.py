from scapy.all import IP, UDP, send, Raw

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

# Definindo as portas
org_port = 12345   # porta de origem
dest_port = 50000   # porta de destino
payload = b'\x02\x5C\xE1'  # payload de 3 bytes

# Cabeçalho IP
src_ip = (187, 64, 55, 75)  # IP de origem
dst_ip = (15, 228, 191, 109)  # IP de destino
ip_header = IP(src='.'.join(map(str, src_ip)), dst='.'.join(map(str, dst_ip)))

# Cabeçalho UDP
udp_header = UDP(sport=org_port, dport=dest_port, len=8 + len(payload), chksum=0)

# Calcular o checksum manualmente
udp_checksum = calculate_udp_checksum(src_ip, dst_ip, udp_header, payload)

# Atualizar o cabeçalho UDP com o checksum calculado
udp_header.chksum = udp_checksum

# Pacote
packet = ip_header / udp_header / Raw(load=payload)  # '/' -> concatenação de camadas do pacote

print("Pacote: ")
packet.show()
