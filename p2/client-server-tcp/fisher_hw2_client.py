#!/usr/bin/env python
'''
author: Steven Fisher
class: CPE 601
time: mw 1:00 pm - 2:15pm
Homework #2
fisher_hw2_client.py
'''

import sys
from socket import *
import time



#s.settimeout(10)
server_ID = sys.argv[1]
server_port  = int(sys.argv[2])
#control = True
server_address = (server_ID, server_port)

#s.connect((server_ID, server_port))
#print 'Sending REGISTER', device_ID, MAC, IP , port
#s.send('REGISTER'+device_ID+MAC+IP+str(port))
#DEREGISTER device-ID MAC
#QUERY code parameter(s)
#QUIT device-ID
while True:
    #time.sleep(5)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_ID, server_port))
    #Menu for client
    print 'Please enter one of the following commands'
    print 'REGISTER device_ID MAC IP port'
    print 'QUERY code parameter(s)'
    print 'MSG from-ID to-ID message'
    print 'DEREGISTER device_ID MAC'
    print 'QUIT device-ID'
    client_input = raw_input()

    command = []                  #initializing command variable
    command = client_input.split()#setting command varible to user input
    #the following check which command was entered
    if command[0] == 'REGISTER':  
        s.sendto(client_input, server_address)        
    elif command[0] == 'QUERY':
        s.sendto(client_input, server_address)
    elif command[0] == 'MSG':
        s.sendto(client_input, server_address)
    elif command[0] == 'DEREGISTER':
        s.sendto(client_input, server_address)
    elif command[0] == 'QUIT':
        s.sendto(client_input, server_address)
        break
    else:                       #executes if user enters an invalid command type
        print 'Please enter a valid command'
    received_server = s.recvfrom(1024) #receives response from server
    print received_server[0]           #displays the response from server
    s.close                            #closes the connection
    #del s
        

s.close
