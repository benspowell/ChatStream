import select, socket, sys, Queue, os

credentials={'user':'pass'}
file = open("credentials", "r")
for line in file:
    cred = line.split("/")
    credentials[cred[0]]=cred[1]
file.close()

myIP = socket.gethostbyname(socket.gethostname())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((myIP, 1270))
server.listen(5)
inputs = [server, sys.stdin]

unauthenticated_sockets = []
online_users = []
socket_list = []
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
        #HANDLING OF INITIAL USER CONNECTIONS
            connection, client_address = s.accept()
            if not shh: print "client connected! address is {}".format (client_address)
            connection.setblocking(0)
            inputs.append(connection)
            socket_list.append(connection)

        elif s is sys.stdin:
        #HANDLING OF SERVER COMMANDS
            newData = 1
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
        #HANDLING OF RECIEVED DATA
            data = s.recv(1024)
            if data:
                #PASSWORD VERIFICATION
                if s in unauthenticated_sockets: 
                    if not shh: print 'login attempt: ' + data
                    attempt = data.split('/')
                    if attempt[0] in credentials:
                        if credentials[attempt[0]] is attempt[1]:
                            online_users.append(attempt[0])
                            if not shh: print attempt[0] + ' - logged in successfully'
                        else:
                            if not shh: print attempt[0] + ' - login failed: invalid password'
                            s.send("invalid password for "+[attempt[0]]+". try again or choose a new username.")
                            s.close()
                    else:
                        file = open("credentials", "a")
                        file.write(attempt[0] + "/" + attempt[1])
                        file.close()
                        if not shh: print attempt[0] + ' - new account created'
                        online_users.append(attempt[0])
                else:
                    if not shh: print "recieved message: " + data
                
                #MESSAGE PROCESSING
                online_string = 'online now: '
                for user in online_users:
                    online_string += user + "   "
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

