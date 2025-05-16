# Import libraries
import time
import tkinter
from tkinter import Button, PhotoImage, Label

from CubeObject import Cube
from connectionsManager import connectionsManager
from Blocks import *
import pickle
import threading





class MainWindow(tkinter.Frame):
    """
    class for the main window. Controls all the UI elements and other windows.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent                        # tkinter root
        self.parent.title("Thorlabs Sisenik")     # naming the app

        ico = Image.open('cube.png')
        photo = ImageTk.PhotoImage(ico)
        self.parent.wm_iconphoto(False, photo)

        self.options = ["pump","probe"]
        self.calibrateWindowOpened = False
        self.runWindowOpen = False

        self.parent.minsize(900, 600)               # setting the size of the window
        self.parent.maxsize(900, 600)
        self.parent.resizable(False, False)         # disable scaling

        self.manager = connectionsManager()         # manager that controls connections
        self.cubes = []                             # list of all the connected cubes
        self.namePairs = {}                         # dictionary to store all the names and serial numbers

        parent.protocol('WM_DELETE_WINDOW', self.closeFunct)    # function that calls when main window is being closed

        self.checkConnectionsVar = False
        with open("manual.txt","r") as f:
            self.manualText = f.read()

        thread = threading.Thread(target=self.checkConnections)
        thread.start()


        """
        All the UI elements and functions that are called on creation of main window
        """

        self.refreshButton = Button(self.parent, text = "Refresh", command=self.__refresh) # button to refresh all the connections
        self.initWindow()     # scans all the connections and creates ui for

    def checkConnections(self):
        return

        while True:
            if self.checkConnectionsVar:
                for i in self.cubes:
                    print(i.controller.LoadMotorConfiguration(
                        i.serialNumber,
                        i.dc
                    ))

                    connected = (i.controller is not None)

                    if not connected:
                        PopupWindow("device " + i.serialNumber + " disconnected")

            time.sleep(1)

    def __refresh(self):      # refresh function. Is being called from the refresh  button
        self.listCubes.destroy()        # destroy old UI so it can be replaced
        self.buttonINIT.destroy()
        self.refreshButton.destroy()

        self.refreshButton = Button(self.parent, text = "Refresh", command=self.__refresh) # button to refresh all the connections

        self.initWindow()

    def initWindow(self):       # main function for creating the INIT window. Handles all the UI elements and communication with the dll libraries
        self.connectAllCubes()  # creates list of all the connected cubes

        self.loadOldNames()     # loads dictionary with all the serial number/name pairs

        for cub in self.cubes:
            if not cub.serialNumber in set(self.namePairs.keys()):
                self.namePairs[cub.serialNumber] = [cub.name, cub.myType]    # adds all the serial numbers that didn't exist in the dictionary before


        for cub in self.cubes:      # sets the names so they can be displayed later
            cub.oldName = self.namePairs[cub.serialNumber][0]
            cub.myType = self.namePairs[cub.serialNumber][1]
            cub.allNames = list(set(v[0] for v in self.namePairs.values()))
            cub.allNames.append("new name")

        self.listCubes = ScrollableLayerListInit(self.parent, self)     # creates UI element that lists all the connected cubes and allows user to change their names
        self.listCubes.place(x=20,y=20,height=520,width=860) # places the list
        self.buttonINIT = Button(self.parent, text="INIT",command=self.initializeAllCubes)  # button that starts initialization
        self.buttonINIT.place(x=340,y=555,height=30,width=100)
        self.refreshButton.place(x=460,y=555,height=30,width=100)     # place the refresh button


    def scan(self):         # scans for all the connected cubes
        avaliabeCubes = self.manager.getAllConnectedCubes()

        return avaliabeCubes

    def connectAllCubes(self):  # creates list of all the connected cubes and assignes them their
        asn = self.scan()
        self.cubes = []

        for i in asn:
            self.cubes.append(Cube(self))

            self.cubes[-1].setSerialNumber(i)

    def initializeAllCubes(self):   # starts the initialization process
        self.listCubes.destroy()    # destroy the old UI elements
        self.buttonINIT.destroy()
        self.refreshButton.destroy()

        self.parent.update() # update the UI visuals

        threads = []

        for i in self.cubes:    # start the initialization process with all the cubes
            i.name = i.oldName

            threads.append(threading.Thread(target=i.initializeCube))  # may take some time
            threads[-1].start()

        running = True

        while running:
            running = False

            for i in threads:
                if i.is_alive():
                    running = True

            self.parent.update()


        self.checkConnectionsVar = True
        self.mainWindowOpen()   # function to create all the main window elements

    def disconnectAll(self):    # disconnects all the cube
        for i in self.cubes:
            i.disconnect()      # calls the disconnect function the Cube object

    def mainWindowOpen(self): # handles the main window after init
        self.createButton()     # provizorni

        self.scrollDownMainWindow = ScrollableLayerListMainWindow(self.parent, self)
        self.scrollDownMainWindow.place(x=20,y=150, width=860, height=430)

    def settingsButtonOnClick(self):
        self.destroyButtons()

        self.listCubes = ScrollableLayerListSettings(self.parent, self)     # creates UI element that lists all the connected cubes and allows user to change their names
        self.listCubes.place(x=20,y=20,height=530,width=860) # places the list
        self.closeButton = Button(self.parent, text="Close",command=self.exitSettings)  # button that starts initialization
        self.closeButton.place(x=400,y=565,width=100,height=30)

    def exitSettings(self):
        self.listCubes.destroy()
        self.closeButton.destroy()
        self.mainWindowOpen()


    def calibrate(self):        # creates the calibration window
        if (self.calibrateWindowOpened):    # can't open two windows
            return

        self.calibrateWindowOpened = True
        self.calWindow = CalibrationWindow(self.parent, self)

    def saveOldNames(self):     # save all the ser. numer / name pairs
        with open('ConnectedDevices.pkl','wb') as dic:
            pickle.dump(self.namePairs, dic)
            print("dictionary saved")

    def loadOldNames(self):     # load all the save ser. number / name pairs
        with open('ConnectedDevices.pkl','rb') as dic:
            self.namePairs = pickle.load(dic)
            print("loaded")

    def closeFunct(self):       # handles closing the window
        self.checkConnectionsVar = False # stop the loop
        self.disconnectAll()    # disconnect all cubes
        self.saveOldNames()     # save all the names
        self.parent.destroy()   # destroy root (main loop)



    def createButton(self):     # rewrite later, temporary
        self.mwButtons = []
        self.mwButtons.append(tkinter.Button(self.parent, text="MANUAL", command=self.openManual))
        self.mwButtons[-1].place(x=20,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="SETTINGS", command=self.settingsButtonOnClick))
        self.mwButtons[-1].place(x=120,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="CALIBRATE", command=self.calibrate))
        self.mwButtons[-1].place(x=220,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="MEASURE", command=self.measure))
        self.mwButtons[-1].place(x=320,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="QUIT", command=self.closeFunct))
        self.mwButtons[-1].place(x=420,y=100,width=100)
        self.img = ImageTk.PhotoImage(Image.open("thorlabsLogo.png").resize((384, 60)))
        self.mwButtons.append(tkinter.Label(self.parent, image=self.img))
        self.mwButtons[-1].place(x=20,y=20)



    def move(self):     # remove later, temporary
        for i in self.cubes:
            i.move_to_position(90)

    def destroyButtons(self):       # rewrite later, temporary
        for i in self.mwButtons:
            i.destroy()
        self.scrollDownMainWindow.destroy()

    def eraseNamesDic(self):        # erase all saved names in dict ser. number / name
        self.namePairs = {}

    def measure(self):
        self.mv = Measure(self.parent, self)

    def checkPopup(self, parent, angle):
        popup = PopupWindow(parent,"Check if current possition is 0\nIf not, calibrate again.")

    def openManual(self):
        self.destroyButtons()

        self.manual = scrollableManual(self.parent, self, self.manualText)
        self.closeButtonManual = tkinter.Button(self.parent,text="Close",command=self.closeManual)

        self.manual.place(x=20, y= 100, width=860, height=400)
        self.closeButtonManual.place(x=400, y=560, height=30,width=100)
        self.manualHeader = tkinter.Label(text=(open("manual.txt",'r').read().split("\n")[0]), font=tkinter.font.Font( family="Arial", size=20))
        self.manualHeader.place(x=350,y=20,width=200,height=80)

    def closeManual(self):
        self.closeButtonManual.destroy()
        self.manual.destroy()
        self.manualHeader.destroy()
        self.mainWindowOpen()


class CalibrationWindow(tkinter.Toplevel):  # window class that handles the calibration process
    def __init__(self, parent, mainWindow):
        super().__init__(parent)
        self.mw = mainWindow        # main window reference
        self.title("Calibration")   # title
        self.geometry("750x400")

        self.protocol("WM_DELETE_WINDOW", self.closed)

        self.transient(parent)
        self.grab_set()

        self.listConnectedCubes()   # function that creates all the UI elements

    def listConnectedCubes(self):
        self.layer_list = ScrollableLayerListCal(self, self.mw)
        self.layer_list.pack(fill="both", expand=True, padx=10, pady=10)

    def closed(self):
        self.mw.calibrateWindowOpened = False
        self.grab_release()
        self.destroy()


class PopupWindow(tkinter.Toplevel):
    def __init__(self, parent, _message):
        super().__init__(parent)
        self.title("Message")
        self.geometry("300x100")

        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text=str(_message)).pack(pady=10)
        ttk.Button(self, text="Close", command=self.on_close).pack()

    def on_close(self):
        self.grab_release()
        self.destroy()

class Measure(tkinter.Toplevel):
    def __init__(self, parent, mainWindow):
        super().__init__(parent)
        self.running = False
        self.mw = mainWindow        # main window reference
        self.title("Measure")   # title

        self.transient(parent)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.closed)
        self.parent = parent
        self.resizable(True, False)
        self.geometry("600x400")

        prev_values = self.load_data()

        options = []

        for i in self.mw.cubes:
            _type = i.myType

            if (_type > len(options) - 1):
                for x in range(len(options) - 1, _type):
                    options.append([])

            options[_type].append("<" + i.serialNumber + "> " + i.name)

        numberOfOptions = 2

        for i in range(len(options), numberOfOptions):
            options.append([])

        manager1 = SharedOptionManager(options[0])
        manager2 = SharedOptionManager(options[1])

        self.states = [u"Pol", u"λ/2", u"λ/4 cw",u"λ/4 ccw"]

        self.line_a = OptionLine(self, line_id="A", option_manager=manager1,previous_values=prev_values[0],possibleStates=self.states,previous_states=prev_values[2],prev_enabled=prev_values[4])
        self.line_a.place(x=20,y=50, height=100,width=560)

        self.line_b = OptionLine(self, line_id="B", option_manager=manager2, previous_values=prev_values[1], possibleStates=self.states,previous_states=prev_values[3],prev_enabled=prev_values[5])
        self.line_b.place(x=20,y=250, height=100,width=560)


        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=14)
        CUSTUM_FONT2 = tkinter.font.Font(family="Arial", size=12)

        self.header1 = tkinter.Label(self, text= "PUMP",font=CUSTUM_FONT)
        self.header2 = tkinter.Label(self, text = "PROBE", font=CUSTUM_FONT)

        self.header1.place(x=20,y=15,height=30)
        self.header2.place(x=20,y=215,height=30)

        self.rotationUI = [tkinter.Label(self, text="Rotation:", font=CUSTUM_FONT),
                           tkinter.Label(self, text="Rotation:", font=CUSTUM_FONT),
                           tkinter.Entry(self),
                           tkinter.Entry(self),
                           tkinter.Button(self,text="Run",command=self.run)
                           ]

        self.rotationUI[0].place(x=20,y=160,width=100)
        self.rotationUI[1].place(x=20,y=360,width=100)
        self.rotationUI[2].place(x=120,y=160,width=100)
        self.rotationUI[3].place(x=120,y=360,width=100)
        self.rotationUI[4].place(x=480,y=360,width=100)

    def run(self):
        values1 = self.line_a.get_dropdown2()
        values2 = self.line_b.get_dropdown2()

        inpts = [self.rotationUI[2].get(), self.rotationUI[3].get()]

        try:
            inpts[0] = int(inpts[0])
        except:
            inpts[0] = 0

        try:
            inpts[1] = int(inpts[1])
        except:
            inpts[1] = 0

        precalculatedValues = [[inpts[0],0,0,0],
                               [inpts[1],0,0,0]]

        for i in range(0,3):
            if (values1[i] == self.states[0]):
                precalculatedValues[0][i+1] = precalculatedValues[0][0]
            elif (values1[i] == self.states[1]):
                precalculatedValues[0][i+1] = precalculatedValues[0][0] / 2
            elif (values1[i] == self.states[2]):
                precalculatedValues[0][i+1] = 90
            elif (values1[i] == self.states[3]):
                precalculatedValues[0][i+1] = 270

            if (values2[i] == self.states[0]):
                precalculatedValues[1][i+1] = precalculatedValues[1][0]
            elif (values2[i] == self.states[1]):
                precalculatedValues[1][i+1] = precalculatedValues[1][0] / 2
            elif (values2[i] == self.states[2]):
                precalculatedValues[1][i+1] = 90
            elif (values2[i] == self.states[3]):
                precalculatedValues[1][i+1] = 270

        cubes = []  # Here I get references to the cubes as they are in the dropdowns
        names = [self.line_a.get_selected_values(), self.line_b.get_selected_values()]  # Here I store all the names I have selected in the dropdowns

        allCubesPairs = []

        for i in range(6):
            cubes.append(None)

        for i in self.mw.cubes:
            allCubesPairs.append(("<" + i.serialNumber + "> " + i.name, i))

        for i in range(len(names[0])):
            for g in range(len(allCubesPairs)):
                if (names[0][i] == allCubesPairs[g][0]):
                    cubes[i] = allCubesPairs[g]

        for i in range(len(names[1])):
            for g in range(len(allCubesPairs)):
                if (names[1][i] == allCubesPairs[g][0]):
                    cubes[i+3] = allCubesPairs[g]

        print(cubes)

        threads = []

        for i in range(3):
            if cubes[i] is not None:
                threads.append(threading.Thread(
                    target=lambda c=cubes[i][1], val=precalculatedValues[0][i + 1]: c.move_to_position(val)
                ))
                threads[-1].start()

        for i in range(3):
            if cubes[i + 3] is not None:
                threads.append(threading.Thread(
                    target=lambda c=cubes[i + 3][1], val=precalculatedValues[1][i + 1]: c.move_to_position(val)
                ))
                threads[-1].start()



        self.running = True
        self.rotationUI[4].config(state=DISABLED)

        while self.running:
            self.running = False

            for i in threads:
                if i.is_alive():
                    self.running = True

            self.parent.update()

        self.running = False
        self.rotationUI[4].config(state=ACTIVE)


    def closed(self):
        if self.running:
            return

        self.save_data()
        self.grab_release()
        self.destroy()

    def save_data(self):
        save_list = [self.line_a.get_selected_values(), self.line_b.get_selected_values(),self.line_a.get_dropdown2(),self.line_b.get_dropdown2(),
                     self.line_a.get_enabled(), self.line_b.get_enabled()]

        with open('selected_values.bin', 'wb') as f:
            pickle.dump(save_list, f)

    def load_data(self):
        with open('selected_values.bin', 'rb') as f:
            load_list = pickle.load(f)

        return load_list



