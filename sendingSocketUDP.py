from socket import *

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

while (True):
    menssage,clienteAddress = serverSocket.recvfrom(2048) #recebe a mensagem e o endereço do cliente 
    if(menssage.decode("utf-8")== "quit"):
        print("Saindo...")
        break
    print("Endreço do cliente",clienteAddress)
    print("Mensagem vinda do clinete: ",menssage.decode("utf-8"))
    
    menssageAux = "sever: " + menssage.decode("utf-8")
    serverSocket.sendto(bytes(menssageAux,'ascii'),clienteAddress)