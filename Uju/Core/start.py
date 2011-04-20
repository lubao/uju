#!/usr/bin/env python
'''
Created on 2010/1/17
@author Paul
'''
from socket import socket 
from socket import AF_INET 
from socket import SOCK_DGRAM
from Core import Uju
from SQLEng import SQLEng
import sys
if __name__ == '__main__':
    HOST = "localhost"
    PORT = 20000
    BUF = 1024
    ADDR = (HOST, PORT)
    UDP_SOCK = socket(AF_INET, SOCK_DGRAM)
    UDP_SOCK.bind(ADDR)
    DB_ENG = SQLEng()
    #UJU = Uju()
    #UJU.start()
    try:
        while True:
            print "UDP server running"
            REC_ID, IP_ADDR = UDP_SOCK.recvfrom(BUF)
            print "{0} from {1}".format(REC_ID, IP_ADDR)
            # ((Text,Sender,UDH),)
            REC_DATA = DB_ENG.getMsg(REC_ID)
            UJU = Uju(REC_DATA[0][1], REC_DATA[0][0])
            UJU.daemon = True
            UJU.start()
    except KeyboardInterrupt:
        print "Keyboard Interrupt -Closing Server"
        UDP_SOCK.close()
        sys.exit(1)
