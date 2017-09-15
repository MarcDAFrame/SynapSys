print('utils')

import time
import os
import datetime

def fileWriter(array, file):
    f = open(file, 'w+')
    for item in array:
        f.write("%s\n" % item)

def fileReader(file):
    with open(file) as f:
        content = f.readlines()
    for i in range(len(content)):
        content[i] = content[i].rstrip('\n')
    return content

#fileWriter([1,2,3],'new.txt') #it creates files!

def measureTime(a, args):
    if(args == None):
        start = time.clock()
        holder = a()
    else:
        start = time.clock()
        holder = a(args)
    elapsed = time.clock()
    elapsed = elapsed - start
    print("METHOD NAME: " + a.__name__ + " TIME ELAPSED: ", elapsed)
    return holder
def test():
    print('test')


def logWriter(message, thepath):
    path = thepath + str(datetime.date.today())
    
    if(os.path.exists(path)):#checks if file exists
        temp = fileReader(path)#reads previous points of file
        temp.append(str(datetime.datetime.now()) + ' | ' + message[:])
        fileWriter(temp, path)#writes file
    else: #checks if file doesnt exist
        fileWriter([str(datetime.datetime.now()) + ' | ' + message[:]], path) #creates file

def ticketCreater():
    ticket = fileReader('saves/tickets/tickets')
    new = int(ticket[0]) + 1
    fileWriter([new], 'saves/tickets/tickets')
    return str(new)

def IDESave(fileName, textInput):
    #print('IDESave' + textInput)
    textList = textInput.split('\n')
    fileWriter(textList,fileName)
    codeValue = fileReader('startStream.py')
    textInputList = textInput.split('\n')
    codeValue = codeValue[:codeValue.index('def main(methodsList, twigConnect, settings):')+1]
    for i in range(len(textInputList)):
        textInputList[i] = '\t' + textInputList[i]
    fileWriter(codeValue + textInputList, 'startStream.py')

def IDESaveCode(fileName, textInput):
    #print('IDESave' + textInput)
    textList = textInput.split('\n')
    fileWriter(textList,fileName)
    codeValue = fileReader('startStream.py')
    textInputList = textInput.split('\n')
    codeValue = codeValue[:codeValue.index('def main(methodsList, twigConnect, settings):')+1]
    for i in range(len(textInputList)):
        textInputList[i] = '\t' + textInputList[i]
    fileWriter(codeValue + textInputList, 'startStream.py')



