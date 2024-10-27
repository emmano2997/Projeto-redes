from scapy.all import IP, UDP, Raw, send
import struct

# Função para calcular o checksum manualmente
def calculate_udp_checksum(ip_header, udp_header, payload):
    # Converte os endereços IP para bytes
    source_ip = bytes(map(int, ip_header.src.split('.')))
    dest_ip = bytes(map(int, ip_header.dst.split('.')))
    
    # Construção do pseudo-header
    pseudo_header = source_ip + dest_ip + struct.pack("!BBH", 0, ip_header.proto, udp_header.len)
    
    # Cabeçalho UDP com checksum temporariamente 0
    udp_header_bytes = struct.pack("!HHHH", udp_header.sport, udp_header.dport, udp_header.len, 0)
    data = pseudo_header + udp_header_bytes + payload
    
    # Calcula a soma dos pares de 16 bits (2 bytes)
    checksum = 0
    for i in range(0, len(data), 2):
        part = (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
        checksum += part

    # Adiciona os valores de carry e faz complemento de 1
    checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF

    return checksum

# Definindo as portas
org_port = 12345   # Porta de origem
dest_port = 50000  # Porta de destino
payload = b'\x02\x5C\xE1'  # Payload de 3 bytes

# Cabeçalho IP
ip_header = IP(src='187.64.55.75', dst='15.228.191.109')

# Cabeçalho UDP com checksum inicial 0
udp_header = UDP(sport=org_port, dport=dest_port, len=8 + len(payload), chksum=0)

# Calculando o checksum UDP
udp_checksum = calculate_udp_checksum(ip_header, udp_header, payload)

# Atualizando o checksum calculado no cabeçalho UDP
udp_header.chksum = udp_checksum

# Montando o pacote completo
packet = ip_header / udp_header / Raw(load=payload)

print("Pacote: ")
packet.show()

# Opcional: enviar o pacote
# send(packet)
