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
        self.parent.title("Nějaký jméno co jsem ještě nevymyslel")     # naming the app

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

        for i in threads:
            i.join()

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
        self.closeButton.place(x=400,y=570,width=100,height=20)

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
        self.mwButtons.append(tkinter.Button(self.parent, text="MOVE", command=self.move))
        self.mwButtons[-1].place(x=20,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="SETTINGS", command=self.settingsButtonOnClick))
        self.mwButtons[-1].place(x=120,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="CALIBRATE", command=self.calibrate))
        self.mwButtons[-1].place(x=220,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="MEASURE", command=self.measure))
        self.mwButtons[-1].place(x=320,y=100,width=100)
        self.mwButtons.append(tkinter.Button(self.parent, text="QUIT", command=self.closeFunct))
        self.mwButtons[-1].place(x=420,y=100,width=100)



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


class CalibrationWindow(tkinter.Toplevel):  # window class that handles the calibration process
    def __init__(self, parent, mainWindow):
        super().__init__(parent)
        self.mw = mainWindow        # main window reference
        self.title("Calibration")   # title

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
        self.mw = mainWindow        # main window reference
        self.title("Calibration")   # title

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

        self.line_a = OptionLine(self, line_id="A", option_manager=manager1,previous_values=prev_values[0])
        self.line_a.place(x=20,y=50, height=150,width=560)

        self.line_b = OptionLine(self, line_id="B", option_manager=manager2, previous_values=prev_values[1])
        self.line_b.place(x=20,y=250, height=150,width=560)


        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=14)
        CUSTUM_FONT2 = tkinter.font.Font(family="Arial", size=12)

        self.header1 = tkinter.Label(self, text= "PUMP",font=CUSTUM_FONT)
        self.header2 = tkinter.Label(self, text = "PROBE", font=CUSTUM_FONT)

        self.header1.place(x=20,y=15,height=30)
        self.header2.place(x=20,y=215,height=30)


    def closed(self):
        self.save_data()
        self.grab_release()
        self.destroy()

    def save_data(self):
        save_list = [self.line_a.get_selected_values(), self.line_b.get_selected_values()]

        with open('selected_values.bin', 'wb') as f:
            pickle.dump(save_list, f)

    def load_data(self):
        with open('selected_values.bin', 'rb') as f:
            load_list = pickle.load(f)

        return load_list



