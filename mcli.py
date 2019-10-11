import select, socket, sys, Queue, os
# Echo client program
import socket
import time

count = 0
HOST = sys.argv[1] #raw_input("chat room server ip: ")    # The remote host
PORT = 1270             # The same port as used by the server

os.system("clear")
print 'logging in to chat room.'

username="!@#$"
password="!@#$"

while ((not username.isalnum()) or (not password.isalnum())):
    print 'usernames and passwords should be only alphanumeric characters.'
    print 'enter existing or new username/password.\n'
    username = raw_input('  username: ')
    password = raw_input('  password: ')

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((HOST, PORT))
inputs = [serv, sys.stdin]

serv.sendall(username+"/"+password)

while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is serv:
            data = s.recv(1024)
            os.system("clear")
            print data
	elif s is sys.stdin:
            msg = raw_input()
            serv.sendall(msg)

s.close()
