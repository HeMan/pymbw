#! /usr/bin/env python
# file: pymbw.py
# auth: Jimmy Hedman <jimmy.hedman@southpole.se>
# desc: Simple application to talk to SonyEricsson bluetooth watch MBW-100
#

#from bluetooth import *
import socket
import select
import sys
import time

from watch import parser

myparser = parser()


# Create server for clock to connect to

server = socket.socket(socket.AF_BT, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
print server._sock
channel = socket.bt_rfcomm_get_available_server_channel(server._sock)
#channel = 1
print channel
server.bind(("", channel))
socket.bt_advertise_service(u"Serial", server._sock, True, socket.RFCOMM)
socket.set_security(server._sock, socket.AUTHOR)
server.listen(1)
print "Waiting..."
watch_client, client_info = server.accept()
print "Accepted connection from ", client_info
print dir(watch_client)

fd = None

try:
    while True:
        #(rr,ww,er) = select.select([watch_client,sys.stdin],[],[])
        (rr,ww,er) = select.select([watch_client],[],[])
        for r in rr:
                if r == watch_client:
#                        if fd == None:
#                                fd = watch_client.makefile("rw", 0)
#                        print "nu"
                        data = r.recv(1024, 64)
			print "data1 %s " % data
			while data[-1] != "\n" and data[-1] != "\r":
				data += r.recv(1024, 64)
			
                       # data = fd.readline()
                        print "watch [%s]" % data
                        response = myparser.parse(data)
                        print "response [%s]" % response
                        watch_client.send(response+"\n\r")
                if r == sys.stdin:
                        data = raw_input()
                        watch_client.send(data+"\r")
except IOError,e:
    print "exept"
    print e
    pass

print "disconnected"

watch_client.close()
watch.close()
print "all done"
