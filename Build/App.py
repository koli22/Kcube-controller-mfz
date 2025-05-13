from tkinter import Button

from CubeObject import Cube
from connectionsManager import connectionsManager
from Blocks import *
import pickle




class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("První GUI aplikace")

        self.parent.minsize(900, 600)
        self.parent.maxsize(900, 600)
        self.parent.resizable(False, False)

        self.manager = connectionsManager()
        self.cubes = []
        self.namePairs = {}

        parent.protocol('WM_DELETE_WINDOW', self.closeFunct)
        self.refreshButton = Button(self.parent, text = "Refresh", command=self.__refresh)

        self.initWindow()

    def __refresh(self):
        self.initWindow()


    def initWindow(self):
        self.connectAllCubes()

        self.loadOldNames()

        for cub in self.cubes:
            if not cub.serialNumber in set(self.namePairs.keys()):
                self.namePairs[cub.serialNumber] = cub.name


        for cub in self.cubes:
            cub.oldName = self.namePairs[cub.serialNumber]
            cub.allNames = list(set(self.namePairs.values()))
            cub.allNames.append("new name")

        self.listCubes = ScrollableLayerListInit(self.parent, self)
        self.listCubes.pack(fill="both", expand=True, padx=10, pady=10)
        self.buttonINIT = Button(self.parent, text="INIT",command=self.initializeAllCubes)
        self.buttonINIT.pack(pady=5, padx=10)

        self.refreshButton.pack(pady=5, padx=0)


    def scan(self):
        avaliabeCubes = self.manager.getAllConnectedCubes()

        return avaliabeCubes

    def connectAllCubes(self):
        asn = self.scan()
        self.cubes = []

        for i in asn:
            self.cubes.append(Cube(self))

            self.cubes[-1].setSerialNumber(i)

    def initializeAllCubes(self):
        self.listCubes.destroy()
        self.buttonINIT.destroy()

        for i in self.cubes:
            i.initializeCube()

    def disconnectAll(self):
        for i in self.cubes:
            i.disconnect()

    def calibrate(self):
        self.calWindow = CalibrationWindow(self.parent, self)

    def saveOldNames(self):
        with open('ConnectedDevices.pkl','wb') as dic:
            pickle.dump(self.namePairs, dic)
            print("dictionary saved")

    def loadOldNames(self):
        with open('ConnectedDevices.pkl','rb') as dic:
            self.namePairs = pickle.load(dic)
            print("loaded")

    def closeFunct(self):
        self.disconnectAll()
        self.saveOldNames()
        self.parent.destroy()



    def createButton(self):
        submit_button1 = tkinter.Button(self.parent, text="connect", command=self.connectAllCubes)
        submit_button1.pack(pady=5)
        submit_button2 = tkinter.Button(self.parent, text="init", command=self.initializeAllCubes)
        submit_button2.pack(pady=5)
        submit_button3 = tkinter.Button(self.parent, text="disconnect", command=self.disconnectAll)
        submit_button3.pack(pady=5)
        submit_button3 = tkinter.Button(self.parent, text="calibrate", command=self.calibrate)
        submit_button3.pack(pady=5)

class CalibrationWindow(tkinter.Toplevel):
    def __init__(self, parent, mainWindow):
        super().__init__(parent)
        self.mw = mainWindow
        self.title("Calibration")

        self.listConnectedCubes()

    def listConnectedCubes(self):
        self.layer_list = ScrollableLayerListCal(self, self.mw)
        self.layer_list.pack(fill="both", expand=True, padx=10, pady=10)


