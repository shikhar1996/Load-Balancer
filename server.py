"""
/* -------------------------------------------------------------
 * Authors - Ayush Prakash, Shikhar Agrawal
 * Course Project for Computer Networks 2
 * This is an implementation of a Load Balancer. The theory and
   design are discussed in the report.
 * This file contains code for Server Side.
---------------------------------------------------------------
*/
"""

import socket
import threading
import sys
import json

ports = [1234, 1236, 1238, 1240]
# ports = [1234]


def server_program(index):
    # create TCP socket
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Error: could not create socket")
        print("Description: " + str(msg))
        sys.exit()

    # server.bind(('localhost', ports[index]))
    try:
        # Bind to all interfaces
        server.bind(('localhost', ports[index]))

    except socket.error as msg:
        print("Error: unable to bind on port %d" % ports[index])
        print("Description: " + str(msg))
        sys.exit()

    # server.listen(1)
    # Listen
    try:
        backlog = 1
        # Number of incoming connections that can wait
        # to be accepted before being turned away

        server.listen(backlog)
    except socket.error as msg:
        print("Error: unable to listen()")
        print("Description: " + str(msg))
        sys.exit()

    print("Listening socket bound to port %d" % ports[index])
    print("Server {} online...".format(index+1))

    # print "In accept() state"
    l, addr = server.accept()
    print "Connection to {} established by {}".format(index+1, addr)

    while True:
        try:
            # print "waiting to receive"
            info = l.recv(1024)
            # print "received data from lb"

            client_info = json.loads(info.decode('utf-8'))
            data = client_info['data']
            client_ip = client_info['ip']
            client_port = int(client_info['port'])
            request_type = client_info['type']

            if data == 'quit_now':
                break

	    # print client_ip, client_port
	
            s_client = socket.socket()
            s_client.connect((client_ip, client_port))
            # print "connected to client"

            
            if request_type == 'message':
                print "Confirmation Message sent to client by server ", index+1, "!"
                s_client.send('Message Received!')
                # print "message sent to client"
                s_client.close()

            elif request_type == 'filename':
                print "Sending File to client by server ", index+1
                f = open(data, 'rb') 
                temp = f.read(1024)
                while(temp):
                    s_client.send(temp)
                    temp = f.read(1024)
                s_client.send('DONE!')
                f.close()
                print "File Sent!"

        except socket.error as msg:
            print("Error: unable to accept()")
            print("Description: " + str(msg))
            sys.exit()

    server.close() 


if __name__ == "__main__":
    servers = []  
    for index in range(len(ports)):
        servers.append(threading.Thread(target=server_program, args=(index, )))
        servers[index].start()

    for index in range(len(ports)):
        servers[index].join()

    print "Servers Closed!"
