CHAT ROOM APPLICATION
for cse 3461 project 1
by Ben Powell

dependencies: python 2.7

instructions:
 SERVER:
  -make sure that mserv.py, and credentials are in the same folder
  -run the server with the command: python mserv.py
  -make note of the server's ip address. (it will be printed on the interface)
     -port 1998 is used by default
  -use the server's cli ('help') for more information

 CLIENT:
  -on another machine, run the client, giving the server's ip address as the only command line argument. 
     -example: python mcli.py 1.2.3.4
  -enter credentials to log in or create an account. if the account does not exist, it will be created. usernames and passwords must be alphanumeric.
  -there is no limit on concurrent sessions per user
  -some accounts have been created already: username/password , ben/osu1234 , dave/ogle
  -other online users will be printed at the top of the screen
  -type your message and press enter to send
  -to log out, type 'logout', and press enter

