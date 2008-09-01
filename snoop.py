#! /usr/bin/env python
# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import select
import sys
import time

from watch import parser

myparser = parser()

myparser.parse("AT*SEAM=\"MBW-100\",13")

# Create server for clock to connect to
watch=BluetoothSocket( RFCOMM )
watch.bind(("",PORT_ANY))
watch.listen(1)

port = watch.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( watch, "My dumper",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
# Connect to phone
if len(sys.argv) < 2:
        print "Error, arg 1 should be bt address"
        exit(0)
else:
        addr = sys.argv[1]

find_serial = find_service( uuid = "1101", address = addr )
serial = find_serial[0]
phone=BluetoothSocket( RFCOMM )
phone.connect((serial['host'], serial['port']))

print "Waiting for connection on RFCOMM channel %d" % port

watch_client, client_info = watch.accept()
print "Accepted connection from ", client_info
#print watch.fileno()

try:
    while True:
	(rr,ww,er) = select.select([watch_client,phone,sys.stdin],[],[])
	for r in rr:
	        if r == watch_client:
                        data = r.recv(1024, 64)
                        print "watch [%s]" % data.strip("\r\n")
	                phone.send(data)
	        if r == phone:
                        data = r.recv(1024, 64)
                        print "phone [%s]" % data.strip("\r\n")
	                watch_client.send(data)
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
