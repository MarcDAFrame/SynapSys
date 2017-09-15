from TOOLKIT import TOOLKIT
from TOOLKIT import utils
from TOOLKIT import twig
from TOOLKIT import leaf
import ast

import threading

def openSocket(ip, port):
    self.leafConn = leaf.leaf(ip, port)
    
def listener():
    print('LISTENING')
    t = threading.Thread(target=listener2)
    t.start()

def listener2():
    transmission = leafConn.listenForMessage()
    readTransmission(transmission)#temp file
    while transmission != 'q' or transmission != '':
        print(transmission + ' TRANSMISSION BOYYYYYYYYYYYYYYYYYYYYYYY')
        
        # t2 = threading.Thread(target= lambda: )
        # t2.start()
        transmission = leafConn.listenForMessage()#values
        values = ast.literal_eval(transmission[transmission.index('|')+1:])
        tempRunner(values)


def readTransmission(transmission):
    #print(transmission)
    print('readTransmission')
    decoded = str(transmission[:transmission.index('|')])
    if(decoded == 'CODE'):
        print('FOUND CODE')

        code = transmission[transmission.index('|')+1:]
        #print(code)
        code = ast.literal_eval(code)
        utils.fileWriter(code, 'temp.py')
    if(decoded == 'VALUES'):
        print('FOUND VALUES')



def tempRunner(values):
    import temp
    
    print(temp.a(values)) #then we need to return this value


def closeSocket():
    print('closeSocket')
    leafConn.closeSocket()

def sendMessage():
    print('sendMessage')
    if(connection):
        test.sendMessage('CODE|'+str(cVALUESodeList))
    else:
        print('no connection')
        #myClient.updateValues(error='no connection')
#import temp
#print(temp.a(67))

commandList = [openSocket, closeSocket, listener]
labelsWordsList=['Leaf Client', 'openSocket', 'closeSocket', 'listener']
myClient = client.leafClient(commandList,labelsWordsList)

print('Done - mainClient.py')


#HERE WE ARE



# print(transmission)
# #print()
# if(str(transmission[:transmission.index('|')]) == 'CODE'):
#     code = transmission[transmission.index('|')+1:]
#     #print(code)
#     code = ast.literal_eval(code)
#     utils.fileWriter(code, 'temp.py')
#     import temp
#     print(str(temp.isPrimeNumber(67)) + ' this works yay') #then we need to return this value


print('Done - mainLeafTest')