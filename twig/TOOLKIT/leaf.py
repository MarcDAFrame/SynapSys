import socket
#leaf is the drone computers
import threading
class leaf:
    def __init__(self, ip, port):
        print('leaf')
        self.host = ip#'192.168.2.31'
        self.port = port
        self.openSocket()

        # t1 = threading.Thread(target=self.listenForMessage)
        # t1.start()
        #self.listenForMessage()
        #self.sendMessage('This is a test leaf message')


    def openSocket(self):
        self.mySocket = socket.socket()
        self.mySocket.connect((self.host,self.port))

    def sendMessage(self, message):
        message = input(" -> ")
        while message != 'q':
            self.mySocket.send(message.encode())
            message = input(" \n -> ")
            

    def listenForMessage(self):
        while True:
            self.data = self.mySocket.recv(1024).decode()
            if self.data != None:
                print ("from connected  Twig: " + str(self.data))
                data = None
                return self.data


    def closeSocket(self):
        print('close socket')
        self.mySocket.close()

        
# test = leaf()
# test.closeSocket()
print('Done - leaf')