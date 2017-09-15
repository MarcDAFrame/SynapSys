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
    path = thepath + 'errors-' + str(datetime.date.today())
    
    if(os.path.exists(path)):#checks if file exists
        temp = fileReader(path)#reads previous points of file
        temp.append(str(datetime.datetime.now()) + ' | ' + message[:])
        fileWriter(temp, path)#writes file
    else: #checks if file doesnt exist
        fileWriter([str(datetime.datetime.now()) + ' | ' + message[:]], path) #creates file

def ticketCreater():
    tickets = fileReader('saves/tickets/tickets')
    last = tickets[len(tickets)]

    return 't#' + str(last+1)