import socket
import time

# Função para exibir o menu e obter a escolha do usuário
def show_menu():
    print("1. Data e hora atual;")
    print("2. Uma mensagem motivacional para o fim do semestre;")
    print("3. A quantidade de respostas emitidas pelo servidor até o momento.")
    print("4. Sair")
    return int(input("Escolha uma opção: "))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("187.64.55.75", 50000)  # Coloque o IP público do servidor aqui, 127.0.0.1 ip da maquina local 

while True:
    option = show_menu()

    # Envia a opção escolhida para o servidor
    client.sendto(str(option).encode(), server_address)

    if option == 4:
        print('Saindo...')
        break

    # Recebe a resposta do servidor
    msg_received_bytes, address_ip_server = client.recvfrom(2048)
    msg_received_str = msg_received_bytes.decode()

    print("Resposta do servidor:", msg_received_str)

client.close()