from scapy.all import *

# Exemplo de captura de pacotes
def captura_pacotes():
    pacotes = sniff(count=10)
    pacotes.show()

if __name__ == "__main__":
    captura_pacotes()
