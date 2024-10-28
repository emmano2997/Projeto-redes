from scapy.all import IP, UDP, Raw, sr1
import random
import struct
import socket

# Configura o IP e a porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.172.164' 
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

def criar_pseudocabecalho(ip_origem, ip_destino, protocolo, tamanho_udp):
    # Converter os endereços IP de string para bytes
    ip_origem_bytes = socket.inet_aton(ip_origem)
    ip_destino_bytes = socket.inet_aton(ip_destino)
    
    # Criar o pseudocabeçalho
    pseudocabecalho = (
        ip_origem_bytes +
        ip_destino_bytes +
        struct.pack('!BBH', 0, protocolo, tamanho_udp)
    )
    
    return pseudocabecalho

def calcular_checksum(data):
    # Adicionar padding se a quantidade de bytes for ímpar
    if len(data) % 2 == 1:
        data += b'\x00'

    # Soma os 16 bits
    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word
        # Wraparound
        total = (total & 0xFFFF) + (total >> 16)
    
    # Complemento de 1
    return ~total & 0xFFFF

def send_request_and_receive_response(tipo):
    # Envia a mensagem e retorna a resposta do servidor
    payload, identificador = create_request(tipo)
    ip = IP(dst=SERVER_IP)
    
    # Monta o pacote UDP
    udp = UDP(sport=org_port, dport=SERVER_PORT, len=8 + len(payload))
    pacote = ip / udp / Raw(load=payload)
    
    # Calcula o checksum UDP manualmente
    udp_length = 8 + len(payload)
    pseudocabecalho = criar_pseudocabecalho(SOURCE_IP, SERVER_IP, socket.IPPROTO_UDP, udp_length)
    checksum_manual = calcular_checksum(
        pseudocabecalho + bytes(pacote[UDP]) + bytes(pacote[Raw])
    )
    
    # Atribui o checksum calculado manualmente
    udp.chksum = checksum_manual
    
    # Atribui o checksum calculado automaticamente pelo Scapy
    checksum_scapy = udp.chksum
    
    # Imprime os checksums
    print(f"Checksum calculado manualmente: {checksum_manual:#04x}")
    print(f"Checksum calculado automaticamente pelo Scapy: {checksum_scapy:#04x}")
    
    # Envia o pacote e espera pela resposta
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
        
        # Verifica se o primeiro byte indica que é uma resposta
        if (conteudo[0] & 0x10) == 0x10:  # Verifica se é uma resposta
            identificador = (conteudo[1] << 8) | conteudo[2]  # Identificador
            tamanho_resposta = conteudo[3]  # Tamanho da resposta
            
            # Imprime o identificador e o tamanho da resposta
            print(f"Identificador: {identificador}, Tamanho da resposta: {tamanho_resposta}")

            if tipo == 0 or tipo == 1:
                # Para tipos 0 e 1, lê a resposta propriamente dita
                resposta_propria = conteudo[4:4 + tamanho_resposta].decode('utf-8').rstrip('\0')
                print(f"Resposta propriamente dita: {resposta_propria}")
            elif tipo == 3:
                # Para tipo 2, a quantidade de respostas é um inteiro de 4 bytes
                if tamanho_resposta == 4:  # Certifique-se de que o tamanho é 4 para tipo 2
                    resposta_texto = int.from_bytes(conteudo[4:8], byteorder='big')
                    print(f"Quantidade de respostas do servidor: {resposta_texto}")
                else:
                    print("Tamanho inválido para a quantidade de respostas.")
        else:
            print("Recebida resposta inválida do servidor.")
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
