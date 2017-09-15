from tkinter import *
from tkinter import ttk

from netifaces import AF_INET
import netifaces as ni
from TOOLKIT import utils
from TOOLKIT import TOOLKIT


import leafConnect


#LEAF CLIENT
class leafClient:
    def __init__(self):
        self.consoleOpen=False
        self.c = {'bg' : '#330000', 'fg' : '#FFF', 'red' : '#800', 'lime' : '#00ff00', 'grey' : 'dimgrey', 'black' : '#000'}


        try:
            self.ip = ni.ifaddresses('wlp2s0')[AF_INET][0]['addr']#wlp2s0
        except:
            utils.logWriter('L004 | Error connecting to network with netifaces |','saves/errors/')
            self.ip = 'Unable to connect to server'
        self.console(self.ip)

        methods = {"console" : self.console, 'enableButtons' : self.enableButtons}
        #this is where we open up the leafConn
        self.leafConn = leafConnect.leafConnect(methods)
        
        #creating, editing, and sizing window
        self.root = Tk()
        self.root.resizable(width=False, height=False)
        #self.root.geometry('{}x{}'.format(500, 500))
        self.root.configure(background=self.c['bg'])

        self.widgetsList = self.widgets()
        self.disableButtons(['CLOSEB'])
        self.render(self.widgetsList)
        
    def widgets(self):
        widgetsList = {} #widgetsList [id, tkinterWidget, row, column, columnspan, rowspan]        widgetsList.append([Label(self.root, textvariable=textVariableList[0], fg='#fff', bg='dimgrey', font=("Courier", 18)),0,0,5,1])
        widgetsList['LEAFL'] = [Label(self.root, text='Leaf Client', bg=self.c['bg'], fg=self.c['fg'], font=("Courier", 18)),0,0,2,1]
        widgetsList['ERRORL'] = [Label(self.root, text='', bg=self.c['bg'], fg = self.c['red'], font=("Courier", 14)),0,2,3,1]
        widgetsList['IPL'] = [Label(self.root, text='HOST', bg=self.c['bg'], fg=self.c['fg']),1,0,1,1]
        widgetsList['HOSTL'] = [Label(self.root, text='PORT', bg=self.c['bg'], fg=self.c['fg']),2,0,1,1]
        widgetsList['IPE'] = [Entry(self.root),1,1,2,1]
        widgetsList['PORTE'] = [Entry(self.root),2,1,2,1]
        widgetsList['OPENB'] = [Button(self.root, text='Open Socket', command= lambda: self.openSocket()),3,1,1,1]
        widgetsList['CLOSEB'] = [Button(self.root, text='Close Socket', command=lambda: self.leafConn.closeSocket()),3,2,1,1]
        #widgetsList['LISTENB'] = [Button(self.root, text='Listener', command=lambda: self.leafConn.threadStarter(self.leafConn.listener, 'listener', None)),3,3,1,1]
        widgetsList['CONSOLE'] = [Text(self.root, width=100, height=8, bg=self.c['black'], fg=self.c['lime']),12, 0, 10, 10]
        return widgetsList


    def openSocket(self):
        ip = self.widgetsList['IPE'][0].get()
        port = self.widgetsList['PORTE'][0].get()
        
        if ip != '' and port != '':
            self.updateText('ERRORL', '')
            try:
                self.leafConn.openSocket(ip, int(port))
                self.leafConn.threadStarter(self.leafConn.listener, 'listener', None)
            except Exception as e:
                self.console('E | Error while attemptint to open socket' + str(e))

        else:
            self.updateText('ERRORL', 'PLEASE INPUT IP AND PORT')

    def render(self, widgetsList):
        widgetsStuff = TOOLKIT.dictToList(widgetsList)
        #self.console(str(widgetsStuff[1][1][0]) + "WORD STUFF")
        for i in widgetsStuff:
            #self.console(i[0])
            i[0].grid(row = i[1], column=i[2], sticky='W', columnspan=i[3], rowspan=i[4], padx = 2, pady=2)
        
        self.consoleOpen = True
        self.widgetsList['CONSOLE'][0].config(state=DISABLED)
        self.root.mainloop()
    
    def disableButtons(self, list):
        if type(list) is str:
            print('test')
            self.widgetsList[list][0].config(state="disabled")
        else:    
            for i in list:
                print('test')
                self.widgetsList[i][0].config(state="disabled")

    def enableButtons(self, list):
        if type(list) is str:
            self.widgetsList[list][0].config(state="normal")
        else:
            for i in list:
                self.widgetsList[i][0].config(state="normal")
    
    def updateText(self, list, txt):
        if type(list) is str:
            self.widgetsList[list][0].config(text=txt)
        else:
            for i in list:
                self.widgetsList[0][0].config(text=txt)

    def console(self, txt):
        print(txt)
        #we should log it too

        if(txt[0:1] is 'E'):
            utils.logWriter(txt,'saves/errors/errors-')
        elif(txt[0:1] is 'L'):
            utils.logWriter(txt,'saves/logs/logs-')

        if(self.consoleOpen):
            self.widgetsList['CONSOLE'][0].config(state=NORMAL)
            self.widgetsList['CONSOLE'][0].insert(END, (str(txt) + '\n'))#
            self.widgetsList['CONSOLE'][0].config(state=DISABLED)


client = leafClient()