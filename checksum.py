from scapy.all import IP, UDP, Raw, send, sniff
import struct

# Definições de IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
SOURCE_IP = '177.37.173.165'  # IP de origem do cliente

# Função para criar uma mensagem de requisição
def create_request(tipo, identificador):
    request_byte_0 = (0 << 4) | (tipo & 0x0F)  # req/res é 0, tipo é passado na função
    request_byte_1 = (identificador >> 8) & 0xFF  # Parte alta do identificador
    request_byte_2 = identificador & 0xFF  # Parte baixa do identificador
    return bytes([request_byte_0, request_byte_1, request_byte_2])

# Função para calcular o checksum UDP manualmente
def calculate_udp_checksum(ip_header, udp_header, payload):
    # Converte os endereços IP para bytes
    source_ip = bytes(map(int, ip_header.src.split('.')))
    dest_ip = bytes(map(int, ip_header.dst.split('.')))
    
    # Construção do pseudo-header
    pseudo_header = source_ip + dest_ip + struct.pack("!BBH", 0, ip_header.proto, udp_header.len)
    
    # Cabeçalho UDP com checksum temporariamente 0
    udp_header_bytes = struct.pack("!HHHH", udp_header.sport, udp_header.dport, udp_header.len, 0)
    data = pseudo_header + udp_header_bytes + payload
    
    # Calcula a soma dos pares de 16 bits (2 bytes)
    checksum = 0
    for i in range(0, len(data), 2):
        part = (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
        checksum += part

    # Adiciona os valores de carry e faz complemento de 1
    checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF

    return checksum

# Função para enviar requisição e receber resposta
def send_request_and_receive_response(tipo):
    identificador = 23777  # Usando o identificador fornecido
    request = create_request(tipo, identificador)

    # Definindo portas e comprimento
    source_port = 59155
    destination_port = SERVER_PORT
    length = 8 + len(request)  # 8 bytes do cabeçalho + tamanho do payload

    # Cabeçalho IP e UDP com checksum inicial 0
    ip_header = IP(src=SOURCE_IP, dst=SERVER_IP)
    udp_header = UDP(sport=source_port, dport=destination_port, len=length, chksum=0)

    # Calculando e definindo o checksum UDP
    udp_checksum = calculate_udp_checksum(ip_header, udp_header, request)
    udp_header.chksum = udp_checksum

    # Criando o pacote completo
    udp_packet = ip_header / udp_header / Raw(load=request)

    # Enviando o pacote
    send(udp_packet)

    print(f"Requisição enviada: Tipo {tipo}, Identificador {identificador}")

    # Espera por uma resposta
    response = sniff(filter=f"udp and src host {SERVER_IP} and src port {SERVER_PORT}", count=1, timeout=15)

    if response:
        response_packet = response[0]
        print(f"Resposta recebida (hex): {response_packet[UDP].payload.load.hex()}")
        print(f"Pacote de resposta completo: {response_packet.show()}")

        # Extrai os campos da resposta
        resposta = response_packet[UDP].payload.load
        tipo_resposta = (resposta[0] >> 4) & 0x0F  # 4 bits de req/res
        identificador_resposta = (resposta[1] << 8) | resposta[2]
        tamanho_resposta = resposta[3]

        try:
            resposta_texto = response[4:4 + tamanho_resposta].decode('ascii')
        except UnicodeDecodeError:
            resposta_numero = struct.unpack('!I', response[4:4 + 4])[0]
            resposta_texto = str(resposta_numero)

        print(f"Tipo de resposta: {tipo_resposta}")
        print(f"Identificador de resposta: {identificador_resposta}")
        print(f"Tamanho da resposta: {tamanho_resposta}")
        print(f"Resposta propriamente dita: {resposta_texto}")
    else:
        print("Tempo esgotado. Nenhuma resposta recebida do servidor.")

# Loop de menu interativo
while True:
    print("\nEscolha o tipo de requisição:")
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
