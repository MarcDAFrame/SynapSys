#preset1
#start() - starts the stream
#startCounter()
#endCounter()
#recordTime(intVar) - records the time  
#
from TOOLKIT import utils
import time
import threading
import ast


timeDict = {}
threadDict = {}
returns = {}
contin = True

def start():
	print('start')

def stop():
	contin = False

def startCounter(id):
	print('startCounter')
	timeDict[id] = time.time()


def endCounter(id):
	print('endCounter')
	if timeDict[id]:
		elapsed = time.time() - timeDict[id]
	return elapsed


def recordTime(intValue):
	print(intValue + 'recordTime')

def getCPUList(connectionsList):
	CPUList = []
	for i in connectionsList:
		if i[0] != None and i[2] is True:#insures there is a connection
			CPUList.append(int(i[0]))
	return CPUList

def getValuesFromFile(file):
	with open(file) as f:
		content = f.readlines()
	for i in range(len(content)):
		content[i] = content[i].rstrip('\n')
	return content

def valueSplitter(values, CPUNum):
	temp = []
	for k in range(CPUNum):
		temp.append([])
	for i,j in enumerate(values):
		temp[i%CPUNum].append(j)
	return temp

def threadStarter(threadName, method, args):
	if args != None:
		threadDict[threadName] = threading.Thread(target=method, args=args)
	else:
		threadDict[threadName] = threading.Thread(target=lambda:method())

	threadDict[threadName].start()
def sendDirectory(twigConnect, cpuNum, cpuLIST, direcotry):
	fileList = os.listdir(directory)
	for f in filesList:
		print(f)

	
	
def sendToLeafs(twigConnect, cpuNum, cpuLIST, message):
	#print(j, i)
	ticket = utils.ticketCreater()
	message['ticket']=ticket
	#this is where we save the message to the ticket file or smthing
	twigConnect.sendMessage(cpuNum, message)#"CODE|"+str(codeList)
	#twigConnect.threadStarter(self.startStream, 'stream' + str(j), {'num' : j, 'pyFileName' : pyFileName, 'valueFileName' : valueFileName, 'cpuNUM' : i, 'cpuLIST' : cpuLIST, 'valueList' : valueList})

def putReturns(data):
	print(data)
	returnDict = ast.literal_eval(data)
	returns[returnDict['ticket']] = returnDict

def main(methodsList, twigConnect, settings):
	import numpy
	import cv2
	import os
	import time

	#startCounter('test')
	#print('TEST STUFF' + str(endCounter('test')))
	CPUList = getCPUList(twigConnect.getConnectionList())
	codeList = getValuesFromFile('faceCode')

	while True:
		for j,i in enumerate(CPUList):
			#open listener here
			os.system("fswebcam picture 100")
			methodsList['console']('picture taken')

			threadStarter(str(i), twigConnect.listener, [i, putReturns])

			image = cv2.imread('picture')
			valueList = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

			shape = valueList.shape
			stringedArray = valueList.tobytes()

			sendToLeafs(twigConnect, i, CPUList, {'method' : 'CODE', 'message' : str(codeList)})
			sendToLeafs(twigConnect, i, CPUList, {'method' : 'RUNCODE', 'message' : stringedArray, 'DataType' : 'img', 'shape' : shape})
		
		time.sleep(1)