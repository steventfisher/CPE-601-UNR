#!/usr/bin/python2

#author: Steven Fisher


import sys
from socket import *
from time import time, ctime, sleep
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



#function to add device to Client tabled
def clientRegister(received_data, received_header):
    device_present = 0
    for elem in client_database:
        print(elem[0])
        if elem[0] == received_header[1]: #checking if the device already exists in table
            device_present = 1
    if device_present == 0:              #if device is not in database, then add to database
        client_entry = received_data.split()
        client_entry.append('online')
        print(client_entry)
        if len(received_header) == 5:
            client_entry[4] = int(client_entry[4])
            client_database.append(client_entry[1:])
            efile = open('Activity.log', 'a')
            efile.write('ACK 1 ' + received_header[1] + ' added to database ' +
                        ctime() + '\n')
            efile.close()
            client.sendto('ACK 1 ' + received_header[1] + ' added to database', address)
        else:                           #in user enters an invalid REGISTRATION command
            efile = open('Error.log', 'a')
            efile.write('NACK 3 INVALID COMMAND ' + ctime() + '\n')
            efile.close()              
            client.sendto('NACK 3 INVALID COMMAND', address)
    else:                              #runs if device is already registered
        count = 0
        print('Device already exists')
        for elem in mailbox_database: #checking for messages for device
            if elem[1] == received_header[1]:
                count += 1
        for elem in client_database:
            if elem[0] == received_header[1]:
                elem[-2] = int(received_header[-1])
                elem[-1] = 'online'

        efile = open('Activity.log', 'a')
        efile.write('ACK 2 ' + received_header[1] + ' succesfully checked for' +
                    'messages' + ctime() + '\n')
        efile.close()
        client.sendto('ACK 2 ' + received_header[1] + ' ' +
                      'Message: ' + str(count) + ' ' + ctime(), address)

def clientDeRegister(received_data, received_header): #runs to deregister device
    device_present = 0
    count = 0
    for elem in client_database:
        if elem[0] == received_header[1]:
            device_present = 1
            break
        count += 1
    if device_present == 1:                        #runs if device was registered
        del client_database[count:count+1]
        efile = open('Activity.log', 'a')
        efile.write('ACK 3 ' + received_header[1] + ' removed from database ' +
                    ctime() + '\n')
        efile.close()
        client.sendto('ACK 3 ' + received_header[1] + ' removed from database'
                      , address)
    else:                                         #runs if device was not registered
        efile = open('Error.log', 'a')
        efile.write('NACK 1 ' + ' ' + received_header[1] +
                      ' address is not registered ' + ctime() + '\n')
        efile.close()      
        client.sendto('NACK 1 ' + ' ' + received_header[1] +
                      ' address is not registered', address)

def clientQuery(received_data, received_header): #query function
    device_found = 0
    if received_header[1] == '1':                #executes if querying for device
        for elem in client_database:
            if elem[0] == received_header[2]:
                efile = open('Activity.log', 'a')
                efile.write('ACK 4Device ' + received_header[0] +
                            ' queried for devices ' + ctime() + '\n')
                efile.close()
                client.sendto('ACK 4 Device: ' + elem[0] + ' IP: ' + elem[1] +
                              ' port: ' + str(elem[3]) + ' status: '
                              + str(elem[4]), address)
                device_found = 1
            else:
                device_found = 0
        if device_found == 0:                  #error for invalid query command
            efile = open('Error.log', 'a')
            efile.write('NACK 2 Device not found ' + ctime())
            efile.write('\n')
            efile.close()
            client.sendto('NACK 2 Device not found', address)
                
    elif received_header[1] == '2':           #executes if querying for messages
        msg = False
        for elem in mailbox_database:
            msg_count = 0
            if elem[1] == received_header[2]:
                client.sendto('Message From: ' + elem[0] + ' TO: ' + elem[1]
                              + ' MESSAGE: ' + elem[2] + ' RECEIVED: '
                              + elem[3], address)
                msg = True
            msg_count += 1
        if msg == True:                      #if messages are present, push to device
            mail_log = open('Activity.log', 'a')
            mail_log.write('Delivered message to ' + elem[0] + ' ' +
                           ctime() + '\n')
            del mailbox_database[msg_count-1]
            mail_log.close()
            print('Mailbox: ')
            print(mailbox_database)
        else:                              #executes if there are no messages for device
            efile = open('Error.log', 'a')
            efile.write('NACK 3 No Messages for device' + ctime())
            efile.write('\n')
            efile.close()            
            client.sendto('NACK 3 You have no messages', address)
    else:                                 #executes if query command is malformed
        efile = open('Error.log', 'a')
        efile.write('NACK 2 INVALID CODE' + ctime())
        efile.write('\n')
        efile.close()
        client.sendto('NACK 2 INVALID CODE', address)

def clientMsg(received_data):            #function to send messages from one device to another
    mailbox_entry = []
    mailbox_temp = received_data.split()
    mailbox_msg = ''
    client_present = 0
    for elem in client_database:        #checking if to-ID is in the client database
        if elem[0] == mailbox_temp[2]:
            client_present = 1
    if client_present == 1:            #if to-ID is present then send message
        mailbox_entry.append(mailbox_temp[1])
        mailbox_entry.append(mailbox_temp[2])
        for i in range(3,len(mailbox_temp)):
            mailbox_msg = mailbox_msg + mailbox_temp[i] + ' '
        mailbox_entry.append(mailbox_msg)
        mailbox_entry.append(ctime())
        mailbox_database.append(mailbox_entry)
        mailbox_entry = []
        client.sendto('ACK 1 Message sent to ' + mailbox_temp[2], address)
    else:                            #if to-ID is not present then display NACK
        efile = open('Error.log', 'a')
        efile.write('NACK 5 ' + mailbox_temp[2] + ' device not registered ' +
                    ctime())
        efile.write('\n')
        efile.close()          
        client.sendto('NACK 5 ' + mailbox_temp[2] + ' device not registered',
                     address)
            

    print(mailbox_database)
    
def clientQuit(received_data):
	i = 0
	quit_temp = received_data.split()
	for elem in client_database:
		if elem[0] == quit_temp[1]:
			elem[-1] = 'offline'

	
	        
server_port = int(sys.argv[1])    #receives argument for port from command line
server_address = ('', server_port) #setting the server_address
devices = 0
server = socket(AF_INET, SOCK_STREAM)  #creating a socket
server.bind(server_address)            #binding the socket
server.listen(5)                      #setting server to listen to at most 5 connections
client_database = []                  #initializing client_database
received_header = []                  #initializing received_header
mailbox_database = []                 #initializing mailbox_database
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)
file1 = drive.CreateFile({'title': 'test.txt'})
file1.SetContentString('IoT Ping/Trace Results\n\n')
file1.Upload()
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    file_id = file1['id']

while devices == 0:
    print('Server IP Address: ' + server_address[0])
    print('Waiting for connection . . .')
    client, address = server.accept()
    print('... connected from:', address)

    received_data = client.recv(1024) #receives command from client
    received_header = received_data.split() #splits command to received_header array

    #the following executes the appropriate function based on command received from client
    if received_header[0] == 'REGISTER':
            clientRegister(received_data, received_header)
        
    elif received_header[0] == 'DEREGISTER':
        clientDeRegister(received_data, received_header)
            
    elif received_header[0] == 'QUERY':
        clientQuery(received_data, received_header)

    elif received_header[0] == 'MSG':
        clientMsg(received_data)
        
    elif received_header[0] == 'QUIT':
		clientQuit(received_data)
                if len(client_database) == 0:
                    devices = 1
    elif received_header[0] == 'CLOUD_START':
        oath_file = open('mycreds.txt' , 'r')
        #print(oath_file.read())
        client.sendto(str(oath_file.read()), address)
        oath_file.close()
    elif received_header[0] == 'GET_ID':
        print(file_id)
        client.sendto(file_id, address)
    elif received_header[0] == 'RESULT_UPDATE':
        result_file = open('results.txt', 'w')
        file2 = drive.CreateFile({'id': file_id})
        result_write = file2.GetContentString()
        result_file.write(result_write)
        result_file.close()
        client.sendto('ACK 7 Results Downloaded to Server', address)
        efile = open('Activity.log', 'a')
        efile.write('ACK 7 Results Downloaded to Server')
        efile.close()
    elif received_header[0] == 'Invalid':
        client.sendto(' ', address)
    print(client_database)

#server.shutdown()
server.close()
