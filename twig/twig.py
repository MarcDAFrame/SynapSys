from TOOLKIT import TOOLKIT
from TOOLKIT import utils
from TOOLKIT import twig

import time
import threading

class twigConnect:
    
    def __init__(self, ip, methodsList):
        #print('mainTwigClient INIT')

        self.connectionCount = 0
        self.methods = methodsList
        self.connectionsList = []
        self.threadDict = {}
        self.ip = ip
        for i in range(5):
            self.connectionsList.append([])
            for j in range(5):
                self.connectionsList[i].append(None)

    def SocketInit(self, num):
        #print('newSocketnStuff ' + str(num))
        self.methods["cpuStatusUpdate"](num+1, "#FF0")
        self.methods["console"]('L004 | Socket INIT CPU#' + str(num))
        self.connectionsList[num][0] = num
        #print(self.connectionsList)
        t = threading.Thread(target= lambda: self.openSocket((num)))
        t.start()

    def closeSocket(self, cpuLIST):
        for i in cpuLIST:
            #print(self.connectionsList)
            #print(self.connectionsList[int(i)])
            #gonna have to send a message to make it close the connection on this side i suppose
            try:
                self.sendMessage(i, {'method' : 'CLOSE'})
                self.connectionsList[int(i)][1].close()
                
                #self.methods['']
                for j in range(5):
                    self.connectionsList[int(i)][j] = None
                    #print('CLEARED: ' + str(self.connectionsList[i]))
            
                self.methods['cpuStatusUpdate'](i+1, '#800')
            except Exception as e:
                self.methods["console"]('E004 | Error while Attempting to close connection ' + str(e))

    def openSocket(self, num):
        try:
            #print('openeing connection')
            self.connectionsList[num][1] = twig.twig(self.ip, (5000+num), self.methods)
            #print('waiting on connection')
            self.connectionsList[num][2] = self.connectionsList[num][1].getConnection()
            self.methods["console"]('L003 | Connection Open ' + str(num))
            self.connectionCount += 1
            self.methods["cpuStatusUpdate"](num+1, "#080")

            # self.methods["console"]('L005 | Opening Listener')
            # try:
            #     self.threadStarter(str(num), self.listener, num)
            # except Exception as e:
            #     self.methods["console"]('E008 | Error opening listener ' + str(e))

        except Exception as e1:
            self.methods["console"]('E002 | WHILE OPENING SOCKET ' + str(e1) +  ' CPU NUM ' + str(num))
            self.methods["cpuStatusUpdate"](num+1, "#800")
        
        

    def start(self, pyFileName, valueFileName):
        self.methods["console"]("L002 | Stream Started")
        settings = {'DataType':'int'}#this is where we will read / get settings
        #this is where we distribute the codeList (check to see if it distributed first?)
        cpuLIST = []
        self.startTime = time.time()
        
        for i in self.connectionsList: 
            if i[0] != None and i[2] is True:#insures there is a connection
                cpuLIST.append(int(i[0]))
        #print(cpuLIST)

        print(cpuLIST)  
        if(settings['DataType'] is 'int'):
            valueList = utils.fileReader(valueFileName)#valueFileName
            valueList = TOOLKIT.valueSpliter(valueList, len(cpuLIST))#cpuLIST
            for j,i in enumerate(cpuLIST):
                #print(j, i)
                self.threadStarter('stream' + str(j), self.startStream, {'num' : j, 'pyFileName' : pyFileName, 'valueFileName' : valueFileName, 'cpuNUM' : i, 'cpuLIST' : cpuLIST, 'valueList' : valueList})


    def startStream(self, valsDict):
        codeList = utils.fileReader(valsDict['pyFileName'])#pyFileName
        print(valsDict['cpuNUM'], valsDict['num'])
        self.sendMessage(valsDict['cpuNUM'], {'method' : 'CODE', 'message' : str(codeList)})#"CODE|"+str(codeList)
        #ticket = utils.ticketCreater()
        #this is where we have to save what it has sent to the ticket
        #print("RUNCODE|" + str(ticket) + '|' + str(valueList)[0:100])
        #self.methods('RUNNINGCODE')
        self.sendMessage(valsDict['cpuNUM'], {'method' : 'RUNCODE', 'ticket' : str(ticket), 'message' : str(valsDict['valueList'][valsDict['num']]), 'DataType' : ''})#"RUNCODE|" + str(ticket) + '|' + str(valueList[num])


    def stop(self):
        self.methods["console"]('L006 | Attempting to Stop Twig Stream')
    

    def sendMessage(self, cpuNUM, messageDict):
        if(self.connectionsList[cpuNUM][1] != None):
            #test.sendMessage('CODE|'+str(codeList))
            self.methods['console']('L00x | Attempting to send message ' +str(messageDict)[0:20] + '...(More Data)' + ' ' + str(cpuNUM))
            self.connectionsList[cpuNUM][1].sendMessage(str(messageDict))
        else:
            self.methods["console"]('E003 | NO CONNECTION WHEN ATTEMPTING TO sendMessage' + str(cpuNUM) +str(messageDict)[0:100])
            #this is where we update text and buttons

    def threadStarter(self, method, threadName, args):
        if args != None:
            self.threadDict[threadName] = threading.Thread(target=lambda:method(args))
        else:
            self.threadDict[threadName] = threading.Thread(target=lambda:method())

        self.threadDict[threadName].start()



    def listener(self, num, putReturns):
        self.methods["console"]('L007 | Attempting to open listener')

        self.data = self.connectionsList[num][1].listener()
        self.data = self.data[0:-4]
        putReturns(self.data)

        self.methods["console"]('L008 | received from twig ' + str(num) + ' ' + str(self.data)[0:100])
        #this is where we put the logging of the self.data stuff
        if self.data == '' or self.data == None:
            return None
        self.methods["console"]('L012 | Logging Data...')
        #self.methods['console']('L00x | Time Elapsed' + str(time.time() - self.startTime))
        try:
            utils.logWriter(str(self.data[0]) + ' ' + str(self.data), 'saves/returns/returns-')
        except Exception as e:
            self.methods["console"]('E004 | Error while logging data ' + str(e))
        
        print('returning')
    
    #GETTERS
    def getConnectionList(self):
        return self.connectionsList#[cpuNUM, boolean, None, None, None]
