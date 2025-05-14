# Import libraries

from tkinter import Button

from CubeObject import Cube
from connectionsManager import connectionsManager
from Blocks import *
import pickle





class MainWindow(tkinter.Frame):
    """
    class for the main window. Controls all the UI elements and other windows.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent                        # tkinter root
        self.parent.title("První GUI aplikace")     # naming the app

        ico = Image.open('cube.jpeg')
        photo = ImageTk.PhotoImage(ico)
        self.parent.wm_iconphoto(False, photo)

        self.options = ["probe", "pump"]
        self.calibrateWindowOpened = False
        self.runWindowOpen = False

        self.parent.minsize(900, 600)               # setting the size of the window
        self.parent.maxsize(900, 600)
        self.parent.resizable(False, False)         # disable scaling

        self.manager = connectionsManager()         # manager that controls connections
        self.cubes = []                             # list of all the connected cubes
        self.namePairs = {}                         # dictionary to store all the names and serial numbers

        parent.protocol('WM_DELETE_WINDOW', self.closeFunct)    # function that calls when main window is being closed


        """
        All the UI elements and functions that are called on creation of main window
        """

        self.refreshButton = Button(self.parent, text = "Refresh", command=self.__refresh) # button to refresh all the connections
        self.initWindow()     # scans all the connections and creates ui for initialization

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
                self.namePairs[cub.serialNumber] = cub.name    # adds all the serial numbers that didn't exist in the dictionary before


        for cub in self.cubes:      # sets the names so they can be displayed later
            cub.oldName = self.namePairs[cub.serialNumber]
            cub.allNames = list(set(self.namePairs.values()))
            cub.allNames.append("new name")

        self.listCubes = ScrollableLayerListInit(self.parent, self)     # creates UI element that lists all the connected cubes and allows user to change their names
        self.listCubes.pack(fill="both", expand=True, padx=10, pady=10) # places the list
        self.buttonINIT = Button(self.parent, text="INIT",command=self.initializeAllCubes)  # button that starts initialization
        self.buttonINIT.pack(pady=5, padx=10)
        self.refreshButton.pack(pady=5, padx=0)     # place the refresh button


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

        for i in self.cubes:    # start the initialization process with all the cubes
            i.name = i.oldName
            i.initializeCube()  # may take some time

        self.mainWindowOpen()   # function to create all the main window elements

    def disconnectAll(self):    # disconnects all the cube
        for i in self.cubes:
            i.disconnect()      # calls the disconnect function the Cube object

    def mainWindowOpen(self): # handles the main window after init
        self.createButton()     # provizorni

    def settingsButtonOnClick(self):
        self.destroyButtons()

        self.listCubes = ScrollableLayerListSettings(self.parent, self)     # creates UI element that lists all the connected cubes and allows user to change their names
        self.listCubes.pack(fill="both", expand=True, padx=10, pady=10) # places the list
        self.closeButton = Button(self.parent, text="Close",command=self.exitSettings)  # button that starts initialization
        self.closeButton.pack(pady=5, padx=10)

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
        self.disconnectAll()    # disconnect all cubes
        self.saveOldNames()     # save all the names
        self.parent.destroy()   # destroy root (main loop)



    def createButton(self):     # rewrite later, temporary
        self.mwButtons = []
        self.mwButtons.append(tkinter.Button(self.parent, text="move", command=self.move))
        self.mwButtons[-1].pack(pady=5)
        self.mwButtons.append(tkinter.Button(self.parent, text="settings", command=self.settingsButtonOnClick))
        self.mwButtons[-1].pack(pady=5)
        self.mwButtons.append(tkinter.Button(self.parent, text="calibrate", command=self.calibrate))
        self.mwButtons[-1].pack(pady=5)

    def move(self):     # remove later, temporary
        for i in self.cubes:
            i.move_to_position(90)

    def destroyButtons(self):       # rewrite later, temporary
        for i in self.mwButtons:
            i.destroy()

    def eraseNamesDic(self):        # erase all saved names in dict ser. number / name
        self.namePairs = {}


class CalibrationWindow(tkinter.Toplevel):  # window class that handles the calibration process
    def __init__(self, parent, mainWindow):
        super().__init__(parent)
        self.mw = mainWindow        # main window reference
        self.title("Calibration")   # title

        self.protocol("WM_DELETE_WINDOW", self.closed)

        self.listConnectedCubes()   # function that creates all the UI elements

    def listConnectedCubes(self):
        self.layer_list = ScrollableLayerListCal(self, self.mw)
        self.layer_list.pack(fill="both", expand=True, padx=10, pady=10)

    def closed(self):
        self.mw.calibrateWindowOpened = False
        self.destroy()






