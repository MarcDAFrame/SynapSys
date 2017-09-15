#twig is the main computer
import socket
import netifaces
from netifaces import AF_INET
import threading
import struct
import time

class twig:
    def __init__(self, ip, port, methods):
        
        self.methods = methods
        self.host = ip #"0.0.0.0"#192.168.1.102
        self.port = port
        #print(netifaces.ifaddresses('wlp2s0')[AF_INET][0]['addr'])
        self.socketOpener()
        
    def socketOpener(self):
        self.mySocket = socket.socket()
        self.mySocket.bind((self.host,self.port))

    def getConnection(self):
        self.mySocket.listen(1)
        self.conn, self.addr = self.mySocket.accept()
        print ("Connection from: " + str(self.addr))

        return True

    def listener(self): 
        print('HERE WE ARE')
        self.methods["console"]('L010 | Attempting to Open Listener')
        #self.mySocket.setblocking(0)
        data = b''
        result = self.conn.recv(65536)
        start = time.time()
        data += result
        while(len(result) > 0):
            if(result[-3:] == b'END'):
                break
            result = self.conn.recv(65536)
            data += result
            
        return data.decode()

        #return ''.join(str(total_data))
    
    def sendMessage(self, message):
        #message = str(struct.pack('>I', len(str(message)))) + '|' + str(message)
        self.conn.sendall((str(message)+'|END').encode())
        
    def socketCloser(self):
        self.conn.close()
    
    def close(self):
        print('close - twig')
        self.conn.close()


#twig = twig(5000)
#twig.socketCloser()
print('Done - Twig')
