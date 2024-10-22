import socket
import math
import random
import string

# função pra gerar uma string aleatória de tamanho específico
def random_str(chars = string.ascii_letters + string.digits, str_length = 10):
    return ''.join(random.choice(chars) for _ in range(str_length))

#AF_INET indica que é um protocolo de endereço IP
#SOCK_DGRAM indica que é um protocolo de transporte UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("", 12345)) # "" é localhost

while True:
    msg_to_answer = ""
    msg_received_str = ""

    print("Esperando por clientes...")
    msg_bytes, address_ip_client = server.recvfrom(248) #248 bytes
    msg_received_str = msg_bytes.decode()
    msg_received_int = int(msg_received_str)

    if msg_received_str != "":
        integer_legth = int(math.log10(msg_received_int))+1
        print("Número recebido do cliente: " + str(msg_received_int) +
            " | Ip do Cliente: " + str(address_ip_client)+
            " | Tamanho do numero recebido do cliente: " + str(integer_legth))

    if integer_legth >= 10:
        msg_to_answer = random_str(str_length = integer_legth)

    elif integer_legth < 10:
        if(msg_received_int % 2) == 0:
            msg_to_answer = "PAR"
    else:
        msg_to_answer = "IMPAR"

    server.sendto(msg_to_answer.encode(), address_ip_client)
    print("Mensagem enviada para o cliente: " + msg_to_answer)

    msg_bytes, address_ip_client = server.recvfrom(248)
    msg_received_str = msg_bytes.decode()
    print("Mensagem recebida do clinete: " + msg_received_str)
    print("#"*67) #separador pro consolelog
