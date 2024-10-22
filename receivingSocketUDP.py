import socket

UDP_IP = "177.37.173.165" #teste local "15.228.191.109"
UDP_PORT = 5010

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) 
    print("received message: %s" % data)