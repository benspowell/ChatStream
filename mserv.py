import select, socket, sys, Queue, os

unauthenticated_sockets = []
online_users = []
socket_list = []
connections = 0

myIP = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server.bind((myIP, 1270))
server.listen(5)
inputs = [server, sys.stdin]
newData = 0
shh = False

message_buffer = "------------------------------------------\n"
online_string=""
output=""

os.system("clear")
print 'Welcome to the chat room server!'
print '(commands: help, shh, quit)\n'
print 'IP:',myIP
print

while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
	    if not shh:
                print "client connected! address is {}".format (client_address)

            connection.setblocking(0)
            inputs.append(connection)
            socket_list.append(connection)


            online_string = 'online now: '
            for cli in socket_list:
                online_string += 'person '
            output = online_string + '\n' + message_buffer
            for cli in socket_list:
                cli.send(output)

        elif s is sys.stdin:
            newData = 1;
            command_string = raw_input()
	    if command_string == 'quit':
		for cli in socket_list:
                    cli.close
		sys.exit()
	    elif command_string == 'help':
		print '\nchat room usage:'
		print '    the server is currently ready for connections'
		print '    for a client to connect, enter server IP as a command line arg'
		print '    ex: python mcli.py',myIP
		print 
		print 'shh: toggle verbose behaviour (printing each message and new connection)'
		print 'quit: exit the server program & close chat\n' 
	    elif command_string == 'shh':
		shh = not shh
	    else:
                print "unknown command:" + command_string
        else:
            data = s.recv(1024)
            if data:
                print "recieved message: " + data
                message_buffer += data + '\n'
		output = online_string + '\n' + message_buffer
                if newData == 1:
                    data = command_string
                    newData = 0
                for cli in socket_list:
                    cli.send(output)


    for s in exceptional:
        inputs.remove(s)
        if s in socket_list:
            socket_list.remove(s)
        s.close()

