import select, socket, sys, Queue, os
# Echo client program
import socket
import time

count = 0
HOST = sys.argv[1] #raw_input("chat room server ip: ")    # The remote host
PORT = 1270             # The same port as used by the server


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((HOST, PORT))
inputs = [serv, sys.stdin]



while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is serv:
            data = s.recv(1024)
            os.system("clear")
            print data
	elif s is sys.stdin:
            command_string = raw_input('>')
            msgToSend = command_string
            serv.sendall(msgToSend)

s.close()
