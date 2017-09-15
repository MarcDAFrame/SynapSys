#leaf is the drone computers
from TOOLKIT import TOOLKIT
from TOOLKIT import utils
from TOOLKIT import leaf

import time
import ast
import struct
import socket
import threading

class leafConnect:
    def __init__(self, methods):
        self.console = methods["console"]
        self.console('L001 | Leaf Connect INIT')
        self.methods = methods
        self.threadDict = {}
        self.functionDict = {'TEST' : self.test, 'CLOSE' : self.closeSocket, 'CODE' : self.codeSaver, 'RUNCODE' : self.runCode}
        
    def openSocket(self, ip, port):
        self.console('L002 | Leaf Attempting to Connect to ' + ip + ':' + str(port))
        self.host = ip#'192.168.2.31'
        self.port = port
        try:
            self.mySocket = socket.socket()
            self.mySocket.connect((self.host,self.port))
            self.console('L003 | Successfully Connected to ' + ip + ':' + str(port))
            self.methods['enableButtons'](['CLOSEB'])
        except Exception as e:
            self.console('E001 | Error while attempting to Open Socket ' + str(e))
    

    def threadStarter(self, method, threadName, args):
        if args != None:
            self.threadDict[threadName] = threading.Thread(target=lambda:method(args))
        else:
            self.threadDict[threadName] = threading.Thread(target=lambda:method())

        self.threadDict[threadName].start()


    def listener(self): 
        self.methods["console"]('L010 | Attempting to Open Listener')
        #self.mySocket.setblocking(0)
        
        while True:
            data = b''
            result = self.mySocket.recv(65536)
            start = time.time()
            data += result
            while(len(result) > 0):
                if(result[-3:] == b'END'):
                    break
                result = self.mySocket.recv(65536)
                data += result

            print('Transmitting Time', str(time.time() - start))
            self.parser(data.decode())
                



    def parser(self, data):
        self.console("L007 | Attempting to Parse" + str(data)[0:50] + '...' + str(data[-50:]))
        #print(message)
        #print(self.data.split('|'))
        #splitData = data.split('|+=|')
        data = data[:-4]

        noArgsList = ['CLOSE'] #ADD ANY METHOD THAT DOESN'T HAVE ARGS


        
        dataDict = ast.literal_eval(data)
        if dataDict['method'] in noArgsList:
            self.functionDict[dataDict['method']]()
        else:
            self.functionDict[dataDict['method']](dataDict)


        #self.functionDict[parsedPrefix](parsedPostfix)
    def runCode(self, dataDict):
        self.console('L009 | Attempting to RUNCODE')
        import temp
        ticket = dataDict['ticket']
        #print(ticket)
        #ticket, parsedPostfix = parsedPostfix.split('|')
        #values = str(dataDict['message'])
        try:
            answer = temp.a(dataDict)
            print(answer)
            # answer.insert(0, ticket)
            self.console('L010 | code run response') #str(answer)[0:100]
            self.sendMessage({'ticket' : ticket, 'message' : answer})
        except Exception as e:
            self.console('L00x | error while attempting to run code ' + str(e))
            pass
        #print(answer)

        #this is where we return the values to twig

    def sendMessage(self, message):
        try:
            self.mySocket.send((str(message) + '|END').encode())
        except Exception as e:
            self.console('E003 | Error while attempting to send message to twig ' + str(e))


    def codeSaver(self, dataDict):
        self.console('L008 | attempting codeSaving')
        #print(parsedPostfix)
        try:
            code = ast.literal_eval(str(dataDict['message']))
            utils.fileWriter(code, 'temp.py')
        except Exception as e:
            self.console('E004 | While attempting to code save ' + str(e))
    

    def test(self, message):
        self.console('THIS WORKS YATYYY' + message)

    def closeSocket(self):
        self.console('L006 | Attempting to Close Socket')
        try:
            self.mySocket.close()
            self.console('L007 | Successfully Closed Socket')
        except Exception as e:
            self.console('E002 | Error While Attempting To Close Socket ' + str(e))
