#! /usr/bin/env python
# file: pymbw.py
# auth: Jimmy Hedman <jimmy.hedman@southpole.se>
# desc: Simple application to talk to SonyEricsson bluetooth watch MBW-100
#

from bluetooth import *
import select
import sys
import time

from watch import parser

myparser = parser()


# Create server for clock to connect to
watch=BluetoothSocket( RFCOMM )
watch.bind(("",PORT_ANY))
watch.listen(1)

port = watch.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( watch, "PyMBW",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                    )
                   

print "Waiting for connection on RFCOMM channel %d" % port

watch_client, client_info = watch.accept()
print "Accepted connection from ", client_info

try:
    while True:
	(rr,ww,er) = select.select([watch_client,sys.stdin],[],[])
	for r in rr:
	        if r == watch_client:
                        data = r.recv(1024, 64).strip("\r\n")
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
