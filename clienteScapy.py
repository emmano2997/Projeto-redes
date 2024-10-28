''' 
Alunos: Anna Livia Freire e Emmanuel Aprígio
Matrículas: 20220060424 e 20220060620

'''

from scapy.all import IP, UDP, Raw, sr1
import random
import struct
import socket

'''
SERVER_IP : IP do servidor
SERVER_PORT: Porta do servidor
org_port: porta de origem
Necessário alterar em outros computadores:
SOURCE_IP: Ip do cliente

'''

SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.172.164' # altera aqui S2
org_port = 12345 

def opcoes():
    op = input("Hello! Digite a sua escolha: ")
    return int(op)

def create_request(tipo):
    ''' 
    Criando request (assim como no socket)
    
    '''
    identificador = random.randint(1, 65535)
    request_byte_0 = (0 << 4) | (tipo & 0x0F) 
    request_byte_1 = (identificador >> 8) & 0xFF  
    request_byte_2 = identificador & 0xFF  
    return bytes([request_byte_0, request_byte_1, request_byte_2]), identificador


def criar_pseudocabecalho(ip_origem, ip_destino, protocolo, tamanho_udp):
    '''
    Criando pseudocabeçalho ip para calcular checksum
    Necessário converter os endereços IP de string para bytes

    '''
    ip_origem_bytes = socket.inet_aton(ip_origem)
    ip_destino_bytes = socket.inet_aton(ip_destino)

    pseudocabecalho = (
        ip_origem_bytes +
        ip_destino_bytes +
        struct.pack('!BBH', 0, protocolo, tamanho_udp)
    )
    
    return pseudocabecalho



def calcular_checksum(data):
    '''
    Adiciona padding se a quantidade de bytes for ímpar
    Wraparound e complemento de 1

    '''
    if len(data) % 2 == 1:
        data += b'\x00'

    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word
        total = (total & 0xFFFF) + (total >> 16)
    
    return ~total & 0xFFFF

def send_request_and_receive_response(tipo):
    '''
    Envia request e retorna response do servidor
    Monta o pacote UDP com cabeçalho manual
    Calcula o checksum UDP manualmente

    '''

    payload, identificador = create_request(tipo)
    ip = IP(dst=SERVER_IP)
    
    udp = UDP(sport=org_port, dport=SERVER_PORT, len=8 + len(payload))
    pacote = ip / udp / Raw(load=payload)
    
    udp_length = 8 + len(payload)
    pseudocabecalho = criar_pseudocabecalho(SOURCE_IP, SERVER_IP, socket.IPPROTO_UDP, udp_length)
    checksum_manual = calcular_checksum(
        pseudocabecalho + bytes(pacote[UDP]) + bytes(pacote[Raw])
    )
    
    udp.chksum = checksum_manual
    checksum_scapy = udp.chksum
    
    # Testando se os checksums estão batendo
    print(f"Checksum calculado manualmente: {checksum_manual:#04x}")
    print(f"Checksum calculado automaticamente pelo Scapy: {checksum_scapy:#04x}")
    
    
    resposta = sr1(pacote, timeout=10)

    if resposta:
        print(f"Requisição enviada (ID: {identificador})")
        return resposta
    else:
        print("Nenhuma resposta do servidor.")
        return None


def receber_resp(resposta, tipo):
    '''
    Processa a resposta recebida com base na opção
    Primeiro byte: request ou resposta
    Para 1 e 2, lê a resposta (Hora ou Mensagem motivacional)
    Para 3, a quantidade de respostas é um inteiro de 4 bytes

    '''
    if resposta and Raw in resposta:
        conteudo = resposta[Raw].load
        
        if (conteudo[0] & 0x10) == 0x10: 
            identificador = (conteudo[1] << 8) | conteudo[2] 
            tamanho_resposta = conteudo[3] 
   
            print(f"Identificador: {identificador}, Tamanho da resposta: {tamanho_resposta}")

            if tipo == 1 or tipo == 2:
                resposta_propria = conteudo[4:4 + tamanho_resposta].decode('utf-8').rstrip('\0')
                print(f"Resposta propriamente dita: {resposta_propria}")
            elif tipo == 3:
                if tamanho_resposta == 4:
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
