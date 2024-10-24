import socket
import time

# Função para obter a data e hora formatadas
def get_current_time():
    current_time = time.localtime()
    return time.strftime("%a %b %d %H:%M:%S %Y", current_time)

# Função para enviar mensagem motivacional
def get_motivational_message():
    return "Seja forte!"

# Inicializa o socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("", 12345))  # "" significa que o servidor escuta em todas as interfaces

# Contador de respostas emitidas pelo servidor
response_count = 0

print("Esperando por clientes...")

while True:
    msg_bytes, address_ip_client = server.recvfrom(248)
    option = int(msg_bytes.decode())

    if option == 1:
        response = get_current_time()
    elif option == 2:
        response = get_motivational_message()
    elif option == 3:
        response = f"{response_count}"
    elif option ==4:
        break
    else:
        response = "Opção inválida."

    # Envia a resposta ao cliente
    server.sendto(response.encode(), address_ip_client)
    response_count += 1
    print(f"Resposta enviada para {address_ip_client}: {response}")
