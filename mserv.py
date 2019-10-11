import select, socket, sys, Queue, os

user_name = []
socket_list = []
online_list = []
connections = 0

myIP = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server.bind((myIP, 1270))
server.listen(5)
inputs = [server, sys.stdin]
newData = 0

os.system("clear")
print '\nWelcome to the chat room server!\n'
print 'your IP:',myIP
print

while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is server:
            print "received a connect request from a client......"
            connection, client_address = s.accept()
            if connections == 0:
                connections = 1
                connection1 = connection
            else:
                connection2 = connection
            print "client connected! ip is {}".format (client_address)
            connection.setblocking(0)
            inputs.append(connection)
        elif s is sys.stdin:
            newData = 1;
            command_string = raw_input()
            print "received:::: " + command_string
        else:
            # this stanza handles already connected sockets (data from clients)
            data = s.recv(1024)
            if data:

                # if this is the first time i've seen this socket
                # i want to add it to an array called 'outputs',
                # i use outputs to allow me to queue data to send
#                s.send ("echo response => " + data)
                print "read " + data
                if newData == 1:
                    data = command_string
                    newData = 0
                s.send ("echo response => " + data)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
