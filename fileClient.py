import socket
import sys
import re
import os
#sys.path.append("./lib")       # for params
import params
from framedSock import framedSend, framedReceive
from encapFramedSock import EncapFramedSock


switchesVarDefaults = (
    (('-s', '--server'), "server", "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

encapSock = EncapFramedSock((s, addrPort))
# needs to be the file we read from

#file = input("File to send: ")
#file = "sampleFile.txt"
file = 'C:/Users/Dgarc/Desktop/os_ex/ex1.txt'


if os.path.exists(file):  # if file exists on client end
    inputFile = open(file, mode="r", encoding="utf-8")
    contents = inputFile.read()

    #print(file)
    #print(contents)

    if len(contents) == 0:
        print('will not send empty file exiting')
        sys.exit(0)  # don't send an empty file

    print("sending file")
    encapSock.send(file,contents, debug)
encapSock.close()  # close socket after sending file