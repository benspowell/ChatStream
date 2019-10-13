import select, socket, sys, Queue, os
# Echo client program
import socket
import time

HOST = sys.argv[1] #raw_input("chat room server ip: ")    # The remote host
PORT = 1998             # The same port as used by the server

os.system("clear")
print 'logging in to chat room...'
print '  enter existing or new username and password.\n'

username=" "
password=" "

while ((not username.isalnum()) or (not password.isalnum())):
    print '  usernames and passwords should be only alphanumeric characters.\n'
    username = raw_input('    username: ')
    password = raw_input('    password: ')

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.connect((HOST, PORT))
inputs = [serv, sys.stdin]

serv.sendall(username+"/"+password)

while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is serv:
            data = s.recv(1024)
            if data: 
                os.system("clear")
                print data
            else: 
                print 'connection lost'
	        sys.exit()
	elif s is sys.stdin:
            msg = raw_input()
            serv.sendall(msg)
    for ex in exceptional:
        print 'connection lost'
	sys.exit()


s.close()

