from tkinter import *
from tkinter import ttk

from netifaces import AF_INET
import netifaces as ni
from TOOLKIT import utils
from TOOLKIT import TOOLKIT
import os

import twig


class twigClient:
    #TWIG CLIENT =============================================
    
    def __init__(self):
        self.consoleOpen = False
        #this is where we do the TWIG STUFF
        #twig = twigConnect.twigConnect()
        self.methodsList = {"console" : self.console, "updateText" : self.updateText, "disableButtons" : self.disableButtons, "enableButtons" : self.enableButtons, "cpuStatusUpdate" : self.cpuStatusUpdate}
        self.c = {'bg' : '#00061a', 'fg' : '#fff', 'red' : '#800', 'lime' : '#00ff00', 'grey' : 'dimgrey', }

        try:
            self.ip = ni.ifaddresses('enp1s0')[AF_INET][0]['addr']#wlp2s0
        except Exception as e:
            try:
                self.ip = ni.ifaddresses('lo')[AF_INET][0]['addr']#wlp2s0
            except Exception as e2:
                self.console('E002 | Error connecting to network with netifaces ' + str(e))
                self.ip = 'Unable to connect to server'
                
        self.twigs = twig.twigConnect(self.ip, self.methodsList)
        self.console(self.ip)

        self.console("L005 | Client Open")
        #creating, editing, and sizing window
        self.root = Tk()
        self.root.wm_title('Twig Client v2.7')
        self.root.resizable(width=False, height=False)

        self.settings = self.settingsFiller('saves/settings', self.root)

        #self.root.geometry('{}x{}'.format(500, 500))
        self.root.configure(background=self.c['bg'])
        
        self.counter = 0
        self.widgetsList = self.widgets()
        
        self.render(self.widgetsList)

        self.consoleOpen = False
        self.console("L006 | Client Closed")
        #CLOSE SOCKETS HERE!!

        connectionList1 = self.twigs.getConnectionList()
        contin = False
        temp =[]
        for i in connectionList1:
            if(i[1]):
                contin = True
                if i[0] != None:
                    temp.append(i[0])
        if contin == True:
            for i in temp:
                self.twigs.sendMessage(i, 'CLOSE|NOW')
            #self.console('E006 | No Connections When Attempting to Start Twig')
            self.twigs.closeSocket(temp)
        
        
    def widgets(self):
        widgetsList = {} #widgetsList [id, tkinterWidget, row, column, columnspan, rowspan]

        menubar = Menu(self.root, bg = self.c['bg'], fg=self.c['fg'], borderwidth=2, font=("arial", 10), activebackground=self.c['fg'])
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, fg=self.c['fg'], bg=self.c['bg'], tearoff=0)
        filemenu.add_command(label="Settings", command=self.settingsOpener)
        filemenu.add_command(label="Export Data", command=self.test)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        windowmenu = Menu(menubar, fg=self.c['fg'], bg=self.c['bg'], tearoff=0)
        windowmenu.add_command(label="Console Preferences", command=self.test)
        windowmenu.add_command(label="IDE -    Code", command=self.IDEOpenerCode)
        windowmenu.add_command(label="IDE - Program", command=self.IDEOpenerProgram)
        windowmenu.add_command(label="Clear Console", command=self.clearConsole)
        
        menubar.add_cascade(label="Window", menu=windowmenu)

        connbar = Menu(menubar, fg=self.c['fg'], bg=self.c['bg'], tearoff=0)
        connbar.add_command(label="Ping Connections", command=self.test)
        connbar.add_command(label="Reset Connections", command=self.test)
        menubar.add_cascade(label="Connections", menu=connbar)

        helpmenu = Menu(menubar, fg=self.c['fg'], bg=self.c['bg'], tearoff=0)
        helpmenu.add_command(label="About", command=self.test)
        helpmenu.add_command(label="Report Error", command=self.test)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)


        widgetsList['TWIGL'] = [Label(self.root, text='Twig Client', fg=self.c['fg'], bg=self.c['bg'], font=("Courier", 18)),0,0,5,1]
        widgetsList['TWIGL2'] = [Label(self.root, text=self.ip, fg=self.c['lime'], bg=self.c['bg'], font=("Courier", 14)),0,2,5,1]

        widgetsList['TWIGLE'] = [Label(self.root, text="", fg='#800', bg=self.c['bg'], font=("Courier", 12)),1,0,5,1]

        widgetsList['ADDCPU'] = [Button(self.root, text='Add Computer', command=lambda: self.addComputer()), 3, 0, 1, 1]
        widgetsList['START'] = [Button(self.root, text='Start', command=lambda: self.startTwig(self.counter)), 3, 1, 1, 1]
        widgetsList['STOP'] = [Button(self.root, text='Stop', command=lambda: self.stopTwig(self.counter)), 3, 2, 1, 1]
        
        widgetsList['PYHOLDL'] = [Label(self.root, text='Enter Python File:', bg=self.c['bg'], fg=self.c['fg']), 10, 0, 2, 1]
        widgetsList['PYHOLDE'] = [Entry(self.root), 10, 1, 3, 1]

        widgetsList['VALUEL'] = [Label(self.root, text='Enter  Value  File:', bg=self.c['bg'], fg=self.c['fg']), 11, 0, 2, 1]
        widgetsList['VALUEE'] = [Entry(self.root), 11, 1, 3, 1]
        widgetsList['CONSOLE'] = [Text(self.root, width=100, height=8, bg="#000", fg=self.c['lime']), 12, 0, 10, 10]
        self.consoleOpen = True
        
        #self.console(widgetsList)
        return widgetsList

    def IDEOpenerCode(self):
        #root init
        t = Toplevel(self.root)
        t.wm_title('IDE')
        t.resizable(width=False, height=False)

        #var init
        omVar = StringVar(t)
        options = os.listdir('saves/IDE/code/')
        savedPreset = 'Cpreset1' #this should be gotten from settings
        omVar.set(savedPreset) # default value
        #print(options)


        #widgets init
        textInput = Text(t, width=70, height=20, bg="#000", fg=self.c['lime'])
        dropDownL = Label(t, text='Presets')
        dropDown = OptionMenu(t, omVar, *options, command = lambda x: self.OptionMenuEvent(omVar, textInput, 'saves/IDE/code/'))
        addBtn = Button(t, text='+', command=self.test)
        saveBtn = Button(t, text='save', command=lambda: utils.IDESaveCode(str('saves/IDE/code/' + omVar.get()), textInput.get("1.0",END)))
        runBtn = Button(t, text='run', command=lambda: self.startTwig(self.counter))

        #textInput
        textInput.focus_set()
        #print(utils.fileReader('saves/IDE/code/' + savedPreset))
        presetTextList = utils.fileReader('saves/IDE/code/' + savedPreset)
        for i in presetTextList:
            textInput.insert(END, i)
            textInput.insert(END, '\n')

        #render
        textInput.grid(row = 0, column = 0, columnspan = 5)
        dropDownL.grid(row = 1, column = 0)
        dropDown.grid(row=1, column = 1)
        addBtn.grid(row=1, column = 2)
        saveBtn.grid(row=1, column=3)
        runBtn.grid(row=1, column=4)



    def IDEOpenerProgram(self):
        #root init
        t = Toplevel(self.root)
        t.wm_title('IDE')
        t.resizable(width=False, height=False)

        #var init
        omVar = StringVar(t)
        options = os.listdir('saves/IDE/program/')
        savedPreset = 'preset1' #this should be gotten from settings
        omVar.set(savedPreset) # default value
        print(options)


        #widgets init
        textInput = Text(t, width=70, height=20, bg="#000", fg=self.c['lime'])
        dropDownL = Label(t, text='Presets')
        dropDown = OptionMenu(t, omVar, *options, command = lambda x: self.OptionMenuEvent(omVar, textInput, 'saves/IDE/program/'))
        addBtn = Button(t, text='+', command=self.test)
        saveBtn = Button(t, text='save', command=lambda: utils.IDESave(str('saves/IDE/program/' + omVar.get()), textInput.get("1.0",END)))
        runBtn = Button(t, text='run', command=lambda: self.startTwig(self.counter))

        #textInput
        textInput.focus_set()
        #print(utils.fileReader('saves/IDE/code/' + savedPreset))
        presetTextList = utils.fileReader('saves/IDE/program/' + savedPreset)
        for i in presetTextList:
            textInput.insert(END, i)
            textInput.insert(END, '\n')

        #render
        textInput.grid(row = 0, column = 0, columnspan = 5)
        dropDownL.grid(row = 1, column = 0)
        dropDown.grid(row=1, column = 1)
        addBtn.grid(row=1, column = 2)
        saveBtn.grid(row=1, column=3)
        runBtn.grid(row=1, column=4)

    def OptionMenuEvent(self, omVar, textInput, path):
        textInput.delete('1.0', END)
        presetTextList = utils.fileReader(path + omVar.get())
        for i in presetTextList:
            textInput.insert(END, i)
            textInput.insert(END, '\n')


    def settingsFiller(self, file, root):
        settings = utils.fileReader(file)
        settingsDict = {}
        for i in settings:
            temp = i.split('|')
            if(temp[2] == 'StringVar'):
                settingsDict[temp[0]] = StringVar()
                settingsDict[temp[0]].set(temp[1])
            else:
                settingsDict[temp[0]] = temp[1]
        return settingsDict

    def test(self):
        self.console('Test')
        
    def startTwig(self, cpuCOUNT):
        self.console("L005 | Attempting to Start Twig with a CPU COUNT of " + str(cpuCOUNT))
        connectionList = self.twigs.getConnectionList()
        contin = False
        #pathDir = os.path.dirname(os.path.abspath(__file__))
        for i in connectionList:
            if(i[1]):
                contin = True
        if contin == False:
            self.console('E006 | No Connections When Attempting to Start Twig')
            return
        
        import startStream
        self.stream = startStream.main(self.methodsList, self.twigs, self.settings)


    def stopTwig(self, cpuCOUNT):
        self.console("LOG | stopTwig")
        # buttonsToBeEnabled = ["START", "ADDCPU"]
        # for i in range(cpuCOUNT):
        #     buttonsToBeEnabled.append("CPUB2#" + str(i+1))
        #     buttonsToBeEnabled.append("CPUB3#" + str(i+1))
            
        #self.enableButtons(buttonsToBeEnabled)
        #commandsList["stop"](self.counter)
        #self.twigs.stop(cpuCOUNT)
        self.stream.stop()

    def addComputer(self):
        if(self.counter < 6):
            self.console('L001 | COMPUTER ADDED | ' +  str(self.counter+1))
            num = self.counter
        
            self.widgetsList['CPUL1#' + str(self.counter+1)] = [Label(self.root, text='CPU #' + str(self.counter+1), fg=self.c['fg'], bg=self.c['bg']), (self.counter+4), 0, 1, 1]
            self.widgetsList['CPUB1#' + str(self.counter+1)] = [Button(self.root, text='CPU #' +str(self.counter+1) + ' console', command=lambda : self.consoleOpener(num)), (self.counter+4), 1, 1, 1]
            self.widgetsList['CPUB2#'+ str(self.counter+1)] = [Button(self.root, text='Open Conn #' +str(self.counter+1), command=lambda : self.twigs.SocketInit(num)), (self.counter+4), 2, 1, 1]
            self.widgetsList['CPUB3#'+ str(self.counter+1)] = [Button(self.root, text='Send Message', command=lambda : self.twigs.sendMessage(num, "Message" + str(num))), (self.counter+4), 3, 1, 1, 1]
            self.widgetsList['CPUB3#'+ str(self.counter+1)] = [Button(self.root, text='Close Socket', command=lambda : self.twigs.closeSocket([num])), (self.counter+4), 4, 1, 1, 1]
            self.widgetsList['CPUF#' +str(self.counter+1)] = [Frame(width=30, height=30, bg=self.c['red'], colormap="new"), (self.counter+4), 5, 1, 1, 1]
            self.widgetsList['CPUB4#'+ str(self.counter+1)] = [Button(self.root, text='Send Message', command=lambda : self.twigs.sendMessage(num, 'TEST|Hay there boyxoxox')), (self.counter+4), 6, 1, 1, 1]

            self.counter += 1
            self.render(self.widgetsList)
        else:
            self.console('E003 | COMPUTER AT MAX QTY OF | ' +  str(self.counter))

    def consoleOpener(self, num):
        t = Toplevel(self.root)
        t.wm_title("Window #%s" % (num+1))
        l = Label(t, text="This is window #%s" % (num+1))

        #ThIS IS WHEERE THE CONSOLE GOES
        text = Text(t, height=8, width=8)#default h = 24, w = 80
        text.insert(END, 'TEST')
        text.pack(side="top", fill="both", expand=True)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)   

    def settingsOpener(self):
        t = Toplevel(self.root)
        t.wm_title('Settings')
        #l = Label(t, text="This is window #%s" % (num+1))

        #ThIS IS WHEERE THE CONSOLE GOES
        MODES = [
            ("INT", "int"),
            ("IMAGE", "img"),
            ("STRINGS", "strings"),
            ("NPARRAY", "nparray"),
        ]



        for text, mode in MODES:
            b = Radiobutton(t, text=text, variable=self.settings['DataType'], value=mode)
            b.pack(anchor=W)


    def render(self, widgetsList):
    
        widgetsStuff = TOOLKIT.dictToList(widgetsList)
        #self.console(str(widgetsStuff[1][1][0]) + "WORD STUFF")
        for i in widgetsStuff:
            #self.console(i[0])
            i[0].grid(row = i[1], column=i[2], sticky='W', columnspan=i[3], rowspan=i[4], padx = 2, pady=2)
        self.widgetsList['CONSOLE'][0].config(state=DISABLED)
        self.root.mainloop()
    
    def disableButtons(self, list):
        if type(list) is str:
            self.widgetsList[list][0].config(state="normal")
        else:    
            for i in list:
                self.widgetsList[i][0].config(state="normal")

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
            self.widgetsList['CONSOLE'][0].see(END)
    def clearConsole(self):
        self.widgetsList['CONSOLE'][0].config(state=NORMAL)
        self.widgetsList['CONSOLE'][0].delete('1.0', END)
        self.widgetsList['CONSOLE'][0].config(state=DISABLED)


    def cpuStatusUpdate(self, cpuNUM, color):
        print('Color Updater')
        self.widgetsList['CPUF#' + str(cpuNUM)][0].config(bg=color)



    def eventHandler(self, method, args, returnVariable):
        if args is None:
            returnVariable = method()
        else:
            returnVariable = method(args)



client = twigClient()
