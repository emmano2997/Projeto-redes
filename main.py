from scapy.config import conf
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send

iface = conf.iface
ip = IP(src=iface.ip, dst='127.0.0.1')  # IP de destino maquina local

# Definindo as portas de origem e destino
udp = UDP(sport=50000, dport=12345)  # Porta de origem (12345) e destino (8080)

data = input(int(""))

send(ip/udp/data)
