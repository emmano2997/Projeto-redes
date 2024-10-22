import socket
import time

# Criar um socket UDP
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definir o endereço do servidor
endereco_servidor = ('187.64.55.75', 12345)  # Substitua <IP_DO_SERVIDOR> pelo IP do computador servidor

# Enviar uma mensagem
mensagem = 'Olá, servidor!'.encode('utf-8')  # Codificando para bytes
cliente_socket.sendto(mensagem, endereco_servidor)

# Aguardar um pouco antes de tentar receber a resposta
time.sleep(1)

# Receber resposta
dados, endereco = cliente_socket.recvfrom(1024)  # Desempacotando corretamente
print(f"Recebido do servidor: {dados.decode('utf-8')}")  # Decodificando a resposta

# Fechar o socket
cliente_socket.close()
