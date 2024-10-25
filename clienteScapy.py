from scapy.all import IP, UDP, send, Raw

# definindo as portas
org_port = 12345   # porta de origem
dest_port = 50000   # porta de destino
payload = b'\x02\x5C\xE1'  # payload de 3 bytes
# 0x025CE1 (req da quant de respostas enviadas pelo server, com id 23777)

# cabeçalho IP
ip_header = IP(src = '187.64.55.75', dst = '15.228.191.109')

# cabeçalho UDP
udp_header = UDP(sport = org_port, dport = dest_port, len=8 + len(payload), chksum=0)
# porta de origem, porta de destino, comprimento do segmento (8 + 3 de payload), checksum que inicia 0

# pacote
packet = ip_header / udp_header / Raw(load = payload)# '/' -> concatenação de camadas do pacotes


print("Pacote: ")
packet.show()
