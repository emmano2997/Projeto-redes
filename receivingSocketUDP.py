from socket import *

inputFiles = input("Entre com o endereço IP e o número da porta: ")

x = inputFiles.split()

if(len(x) < 2):
    print("Usando configuração padrão:")
    severName =  "177.37.173.165"
    severPort = 12345
else:
    severName = x[0]
    severPort = int(x[1])

# Cria o socket usando o protocolo IPV4 e UDP
clienteSocket = socket(AF_INET, SOCK_DGRAM)

while(True):
    message = input("Entre com a mensagem a ser enviada (ou 'quit' para sair): ")
    
    if(message.decode("utf-8")== "quit"):
        print("Saindo...")
        break

    auxMessage = message.encode('utf-8')
    clienteSocket.sendto(auxMessage,(severName,severPort))
    
    modifiedMessage,severAddress = clienteSocket.recvfrom(2048)
    print("Endereço do sevidor: ", severAddress)
    print(modifiedMessage.decode("utf-8"))
clienteSocket.close()