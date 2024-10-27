from scapy.all import IP, UDP, Raw, sr1
import random

# Configura o IP e a porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.173.165' 
org_port = 12345  # Porta de origem


def opcoes():
    op = input("Digite a sua escolha: ")
    return int(op)

def create_request(tipo):
    # Cria a mensagem de requisição
    identificador = random.randint(1, 65535)
    request_byte_0 = (0 << 4) | (tipo & 0x0F)  # req/res e tipo
    request_byte_1 = (identificador >> 8) & 0xFF  # Parte alta do identificador
    request_byte_2 = identificador & 0xFF  # Parte baixa do identificador
    return bytes([request_byte_0, request_byte_1, request_byte_2]), identificador

def send_request_and_receive_response(tipo):
    # Envia a mensagem e retorna a resposta do servidor
    payload, identificador = create_request(tipo)
    ip = IP(dst=SERVER_IP)
    udp = UDP(sport=org_port, dport=SERVER_PORT, len=8 + len(payload))
    pacote = ip / udp / Raw(load=payload)
    
    # Calcula o checksum UDP
    udp.chksum = udp.chksum  # (Scapy calcula automaticamente, TEM Q SER MANUAL)
    
    resposta = sr1(pacote, timeout=5)

    # Exibe o status da resposta recebida
    if resposta:
        print(f"Requisição enviada (ID: {identificador})")
        return resposta
    else:
        print("Nenhuma resposta do servidor.")
        return None

def receber_resp(resposta, tipo):
    # Processa a resposta recebida com base na opção
    if resposta and Raw in resposta:
        conteudo = resposta[Raw].load
        if tipo == 3:
            resposta_texto = int.from_bytes(conteudo[4:], byteorder='big')
            print(f"Quantidade de respostas do servidor: {resposta_texto}")
        else:
            resposta_texto = conteudo[4:].decode('utf-8')
            print(f"Resposta propriamente dita: {resposta_texto}")
    else:
        print("Nenhuma resposta recebida.")

while True:
    resposta = ""
    
    print("\nEscolha o tipo de requisição:")
    print("1. Data e hora atual")
    print("2. Mensagem motivacional para o fim do semestre")
    print("3. Quantidade de respostas emitidas pelo servidor")
    print("4. Sair")
    
    op = opcoes()
    match op:
        case 1:
            resposta = send_request_and_receive_response(0)  
        case 2:
            resposta = send_request_and_receive_response(1)  
        case 3:
            resposta = send_request_and_receive_response(2)  
        case 4:
            print("Saindo...")
            break
        case _:
            print("Opção inválida, tente novamente.")
    
    if resposta:
        receber_resp(resposta, op)
