from socket import *
import time

inputFiles = input("Entre com o endereço IP e o número da porta (ou pressione Enter para usar o padrão): ")
x = inputFiles.split()

if(len(x) < 2):
    print("Usando configuração padrão:")
    serverName =  "177.37.173.165"
    serverPort = 12345
else:
    serverName = x[0]
    serverPort = int(x[1])
    
# protocolo IPV4 usando o UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

print("O servidor está pronto para receber")

response_count = 0
while (True):
    menssage,clientAddress = serverSocket.recvfrom(2048) #recebe a mensagem e o endereço do cliente 
    decoded_message = menssage.decode
    print("Endereço do cliente:", clientAddress)
    print("Mensagem vinda do cliente:", decoded_message)
    
    if decoded_message == "1":
        current_time = time.localtime()
        formatted_time = time.strftime("%a %b %d %H:%M:%S %Y", current_time)
        response = f"Data e hora atual: {formatted_time}"
    elif decoded_message == "2":
        response = "Mensagem motivacional: Seja forte! Você consegue!"
    elif decoded_message == "3":
        response = f"Respostas emitidas pelo servidor até o momento: {response_count}"
    elif decoded_message == "4":
        response = "Saindo..."
        serverSocket.sendto(bytes(response, 'utf-8'), clientAddress)
        break
    else:
        response = "Opção inválida. Tente novamente."
    
    serverSocket.sendto(bytes(response, 'utf-8'), clientAddress)
    response_count += 1