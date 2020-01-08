#!/usr/bin/python2
'''
author: Steven Fisher
class: CPE 601
time: mw 1:00 pm - 2:15pm
Homework #3
fisher_hw3_client.py
'''

import sys
from socket import *
import time
import fcntl
import struct
import random
import subprocess

'''
The getHwAddr was modified from code found at
http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
'''

def getHwAddr(ifname):
    hwsc = socket(AF_INET, SOCK_DGRAM)
    info = fcntl.ioctl(hwsc.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def get_ip_address(ifname):
    ipsc = socket(AF_INET, SOCK_DGRAM)
    return inet_ntoa(fcntl.ioctl(
        ipsc.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def traceroute_udp(addrss):
    p = subprocess.Popen("traceroute " + addrss, stdout = subprocess.PIPE,
                         shell=True)

    (output, err) = p.communicate()

    p.status = p.wait()
    return output

def ping_udp(addrss):
    p = subprocess.Popen("ping -c 5 " + addrss, stdout = subprocess.PIPE, shell = True)

    (output, err) = p.communicate()

    p.status = p.wait()
    return output
    
server_ID = sys.argv[1]
server_port  = int(sys.argv[2])
server_address = (server_ID, server_port)
mac_id = getHwAddr('enp0s3')
ip_addr = get_ip_address('enp0s3')
host_name = gethostname()
port = random.randrange(1025, 65536, 1)

while True:
    #Menu for client
    print '-'*40
    print 'Please enter one of the following commands'
    print '1. REGISTER device_ID MAC IP port'
    print '2. QUERY code parameter(s)'
    print '3. MSG from-ID to-ID message'
    print '4. DEREGISTER device_ID MAC'
    print '5. Commuicate with other devices'
    print '6. QUIT device-ID'
    command = client_input = raw_input('Enter a command(1-6): ')

    if command == '1': #Executes the command to Register the device with the server
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(server_address)
        client_data = 'REGISTER ' + host_name + ' ' + ip_addr + ' ' + mac_id + ' ' + str(port)
        s.sendto(client_data, server_address)
        received_server = s.recvfrom(1024) #receives response from server
        print '-'*40
        print received_server[0]           #displays the response from server
        print '-'*40
        s.close         
    elif command == '2': #Executes the command to Query for messages or another device
        print '1. Query another deivce'
        print '2. Query for available messages'
        query_input = raw_input('Please enter 1 or 2: ')
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(server_address)
        if query_input == '1':               #executes if querying for another deivice
            query_device = raw_input('Please enter the device_ID: ')
            client_data = 'QUERY 1 ' + query_device
            s.sendto(client_data, server_address)
            received_server = s.recvfrom(1024) #receives response from server
            print '-'*40
            print received_server[0]           #displays the response from server
            print '-'*40
            s.close         
        elif query_input == '2':             #executes if querying for messages
            
            client_data = 'QUERY 2 ' + host_name
            s.sendto(client_data, server_address)
            received_server = s.recvfrom(1024) #receives response from server
            print '-'*40
            print received_server[0]           #displays the response from server
            print '-'*40
            s.close
        else:
            print '-'*40
            print 'Invalid Command'
            print '-'*40
            s.sendto('Invalid', server_address)
            s.recvfrom(1024)
            s.close()
    elif command == '3':          #executes if sending message to another device
        msg_device = raw_input('Please enter the device_ID to send the message to: ')
        msg = raw_input('Please enter your message: ')
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(server_address)
        client_data = 'MSG ' + host_name + ' ' + msg_device + ' ' + msg
        s.sendto(client_data, server_address)
        received_server = s.recvfrom(1024) #receives response from server
        print '-'*40
        print received_server[0]           #displays the response from server
        print '-'*40
        s.close         
    elif command == '4':         #executes if deregistering the device from the server
        client_data = 'DEREGISTER ' + host_name + ' ' + mac_id
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(server_address)
        s.sendto(client_data, server_address)
        received_server = s.recvfrom(1024) #receives response from server
        print '-'*40
        print received_server[0]           #displays the response from server
        print '-'*40
        s.close
    elif command == '5':               #executes if communicating to another device
        print '-'*40
        print '1. Sending Data'
        print '2. Receiving Data'
        snd_rec = raw_input("Please enter 1 or 2: ")
        if snd_rec == '1':            #executes if sending data to another device
            print '-'*40
            dst_addr = raw_input("Please enter the destination's IP address: ")
            dst_port = int(raw_input("Please enter the destination's Port number: "))
            print '-'*40
            print '1. Run Ping'
            print '2. Run Traceroute'
            udp_input = raw_input('Please select 1 or 2: ')
            addrss = raw_input('Please enter a url or IP address: ')
            u = socket(AF_INET, SOCK_DGRAM)
            #u.bind(ip_addr, port)
            u.connect((dst_addr, dst_port))
            if udp_input == '1':     #executes if running a ping command
                result = ping_udp(addrss)
                u.sendall('DATA ' + host_name + ' ping ' + result)
                received_device, addr = u.recvfrom(1024)
                print '-'*40
                print received_device
                print '-'*40
                u.close()
                #print result
            elif udp_input == '2':   #executes if running a traceroute command
                result = traceroute_udp(addrss)
                u.sendall('DATA ' + host_name + ' trace ' + result)
                received_device, addr = u.recvfrom(1024)
                print '-'*40
                print received_device
                print '-'*40
                u.close()
                #print result
            else:
                print '-'*40
                print 'Invalid Command'
                print '-'*40
                s.sendto('Invalid', server_address)
                s.recvfrom(1024)
                s.close()
        elif snd_rec == '2':       #executes if device is receiving data from another device
            u = socket(AF_INET, SOCK_DGRAM)
            u.bind((ip_addr, port))
            data, addr = u.recvfrom(12000)
            data_info = data.split()
            file_time = time.strftime("%d %b %Y:%H:%M:%S", time.gmtime())
            file_name = data_info[2] + '_' + data_info[1] + '.dat'
            dat_file = open(file_name, 'a')
            dat_file.write('-'*40 + '\n' + data_info[2] + ' result from '
                           + data_info[1] + ' at ' + file_time + '\n'
                           + '-'*40 + '\n')
            dat_file.write(data[3:])
            dat_file.close()
            print data
            u.sendto('ACK 6 ' + host_name, addr)
            u.close()
        else:
            print '-'*40
            print 'Inavlid Command'
            print '-'*40
    elif command == '6':
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(server_address)
        client_data = 'QUIT ' + host_name
        s.sendto(client_data, server_address)
        s.close
        break
    else:                       #executes if user enters an invalid command type
        print '-'*40
        print 'Please enter a valid command'
        print '-'*40
        s.sendto('Invalid', server_address)
        s.recvfrom(1024)
        s.close()              #closes the connection
        

s.close      #closes the socket
