''' 
Alunos: Anna Livia Freire e Emmanuel Aprígio
Matrículas: 20220060424 e 20220060620

'''
import socket
import struct
import random

'''
SERVER_IP : IP do servidor
SERVER_PORT: Porta do servidor
SOURCE_IP: Ip do cliente

'''
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.172.164'  

def create_request(tipo, identificador):
    request_byte_0 = (0 << 4) | (tipo & 0x0F)
    request_byte_1 = (identificador >> 8) & 0xFF 
    request_byte_2 = identificador & 0xFF 
    return bytes([request_byte_0, request_byte_1, request_byte_2])

'''
Criando request como especificado
o identificador é um número aleatório de 1 a 65535 que mudará a cada request

'''

def send_request_and_receive_response(tipo):
    identificador = random.randint(1, 65535)  
    request = create_request(tipo, identificador)

    '''
    Cria o socket do tipo UDP
    AF_INET indica que é um endereço IP
    SOCK_DGRAM indica que é um socket do tipo UDP

    '''

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(15)
        sock.sendto(request, (SERVER_IP, SERVER_PORT))
        print(f"Requisição enviada: Tipo {tipo}, Identificador {identificador}")

        try:
            response, _ = sock.recvfrom(1024)
            print(f"Resposta recebida (hex): {response.hex()}")

            tipo_resposta = (response[0] >> 4) & 0x0F 
            identificador_resposta = (response[1] << 8) | response[2]
            tamanho_resposta = response[3]

            try:
                resposta_texto = response[4:4 + tamanho_resposta].decode('ascii')
            except UnicodeDecodeError:
                resposta_numero = struct.unpack('!I', response[4:4 + 4])[0]
                resposta_texto = str(resposta_numero)

            print(f"Tipo de resposta: {tipo_resposta}")
            print(f"Identificador de resposta: {identificador_resposta}")
            print(f"Tamanho da resposta: {tamanho_resposta}")
            print(f"Resposta propriamente dita: {resposta_texto}")


        except socket.timeout:
            print("Tempo esgotado. Nenhuma resposta recebida do servidor.")

while True:
    print("Escolha o tipo de requisição:")
    print("1. Data e hora atual")
    print("2. Mensagem motivacional para o fim do semestre")
    print("3. Quantidade de respostas emitidas pelo servidor")
    print("4. Sair")
    
    opcao = input("Digite a sua escolha: ")

    if opcao == '1':
        send_request_and_receive_response(0)
    elif opcao == '2':
        send_request_and_receive_response(1)
    elif opcao == '3':
        send_request_and_receive_response(2)
    elif opcao == '4':
        print("Saindo...")
        break
    else:
        print("Opção inválida, tente novamente.")
