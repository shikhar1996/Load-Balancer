"""
/* -------------------------------------------------------------
 * Authors - Ayush Prakash, Shikhar Agrawal
 * Course Project for Computer Networks 2
 * This is an implementation of a Load Balancer. The theory and
   design are discussed in the report.
 * This file contains code for Client Side.
---------------------------------------------------------------
*/
"""

import socket
import sys
import json
import random

if len(sys.argv) != 3:
    print "Usage: python filename -f/-m file.txt/message"
    sys.exit()

_type = ''

if sys.argv[1] == '-f':
    _type = 'filename'
else:
    _type = 'message'

client_port = random.randint(1000, 4000)

try:
    loadBalancer = socket.socket()
    client = socket.socket()
except socket.error as msg:
    print("Error: could not create socket")
    print("Description: " + str(msg))
    sys.exit()

to_send = {'ip': 'localhost', 'type': _type, 'data': sys.argv[2], 'port': client_port}

j_object = json.dumps(to_send).encode('utf-8')

try:
    loadBalancer.connect(('localhost', 8888))
    print "Connected To server..."
    loadBalancer.sendall(j_object)

    print "Request sent to server!"

    client.bind(('localhost', client_port))
    client.listen(1)

        # print "client socket created"
        # print "In accept state"
    s, addr = client.accept()
        # print "waiting for data"
    if to_send['type'] == 'message':
        data = s.recv(1024)
        print "Message Received: ", data
            # print data
    elif to_send['type'] == 'filename':
        print "Receiving file..."
        f = open(to_send['data'], 'wb')
        l = s.recv(1024)
            # print "received: ", l
        while('DONE!' not in l):
            f.write(l)
            l = s.recv(1024)
                # print "received: ", l
        f.close()
        print "File Transfer Complete!"

except socket.error as msg:
    print("Error: Could not open connection")
    print("Description: " + str(msg))
    sys.exit()

try:
    loadBalancer.close()
    client.close()
    print "GoodBye"
    # print "client socket closed"

except socket.error as msg:
    print("Error: unable to close() socket")
    print("Description: " + str(msg))
    sys.exit()

