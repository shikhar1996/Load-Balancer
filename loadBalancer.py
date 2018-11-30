"""
/* -------------------------------------------------------------
 * Authors - Ayush Prakash, Shikhar Agrawal
 * Course Project for Computer Networks 2
 * This is an implementation of a Load Balancer. The theory and
   design are discussed in the report.
 * This file contains code for loadBalancer.
---------------------------------------------------------------
*/
"""

import socket
import sys
import json

quit_struct = {'data': 'quit_now', 'type': 'quit', 'ip': None, 'port': None}
quit_struct = json.dumps(quit_struct).encode('utf-8')

try:
    loadBalancer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("Error: could not create socket")
    print("Description: " + str(msg))
    sys.exit()

loadBalancer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_ports = [1234, 1236, 1238, 1240]
# server_ports = [1234]
index = -1

server = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for x in range(len(server_ports))]

for x in range(len(server_ports)):
    server[x].connect(('localhost', server_ports[x]))

try:
    loadBalancer.bind(('localhost', 8888))
except socket.error as msg:
    print("Error: unable to bind on port 8888")
    print("Description: " + str(msg))
    sys.exit()

loadBalancer.listen(5)
try:
    while 1:
        (c, addr) = loadBalancer.accept()
        print 'Got connection from ', addr

        data = c.recv(1024)
        # print data
    # if data == 'quit_now':
        # break

        index = (index+1) % len(server_ports)
    # server[index].sendall(data)
    # server[index].sendall(addr)

        server[index].sendall(data)
        # print "message sent to server ", index+1

finally:
    loadBalancer.close()
    for x in range(len(server_ports)):
        server[x].sendall(quit_struct)
        server[x].close()
