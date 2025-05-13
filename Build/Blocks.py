import tkinter
from tkinter import ttk, StringVar, OptionMenu
from tkinter.constants import DISABLED
from tkinter.constants import ACTIVE
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

class LayerItemCal(tkinter.Frame):
    def __init__(self, parent, text, image_path, myCube):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        self.cube = myCube

        # Text Label
        tkinter.Label(self, text=text).grid(row=0, column=0, sticky="w")

        # Image (Placeholder for an image)
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=1, padx=10)

        # Button
        self.button1 = tkinter.Button(self, text="Calibrate", command=self.button_action)
        self.button1.grid(row=0, column=2, padx=5)

    def button_action(self):
        self.entry = tkinter.Entry(self)
        self.entry.grid(row=0, column=3)
        self.cube.controller.Home(60000)

        self.button2 = tkinter.Button(self, text="Enter", command=self.button_action2)
        self.button2.grid(row=0, column=4, padx=5)
        self.button1.config(state=DISABLED)

    def button_action2(self):
        _input = self.entry.get()
        number = -1

        try:
            _input = int(_input)
            if (_input >= 0 and _input < 360):
                number = _input
        except:
            pass

        if (number > -1):
            self.button1.config(state=ACTIVE)

            self.button2.destroy()
            self.entry.destroy()

            self.cube.setOffset(number)


class ScrollableLayerListCal(tkinter.Frame):
    def __init__(self, parent, mw):
        super().__init__(parent)

        self.cubesList = mw.cubes
        self.mw = mw

        # Scrollable canvas
        canvas = tkinter.Canvas(self, width=500, height=300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add several layer items
        for i in range(len(self.cubesList)):
            layer = LayerItemCal(self.scrollable_frame, text=self.cubesList[i].name,myCube=self.cubesList[i], image_path="cube.jpeg")
            layer.pack(fill="x", pady=5)



class ScrollableLayerListInit(tkinter.Frame):
    def __init__(self, parent, mw):
        super().__init__(parent)

        self.cubesList = mw.cubes
        self.mw = mw

        # Scrollable canvas
        canvas = tkinter.Canvas(self, width=500, height=300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add several layer items
        for i in range(len(self.cubesList)):
            layer = LayerItemInit(self.scrollable_frame,myCube=self.cubesList[i], image_path="cube.jpeg")
            layer.pack(fill="x", pady=5)


class LayerItemInit(tkinter.Frame):
    def __init__(self, parent, image_path, myCube):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        self.cube = myCube

        self.serNum=tkinter.Label(self, text=self.cube.serialNumber)
        self.serNum.grid(row=0, column=1, sticky="w")

        self.myName=tkinter.Label(self, text="old name:" + str(self.cube.oldName))
        self.myName.grid(row=0, column=2, sticky="w")

        # Image (Placeholder for an image)
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=0, padx=10)

        self.promena = StringVar(self)
        self.promena.set(self.cube.oldName)

        PARAMETRY = self.cube.allNames

        self.optionBar = OptionMenu(self,self.promena,*PARAMETRY,command=self.changeName)
        self.optionBar.grid(row=0, column=3, padx=5)

    def changeName(self,value):
        self.promena.set(value)
        self.cube.changeName(value)

        if (value == "new name"):
            self.inputField = tkinter.Entry(self)
            self.inputButton = tkinter.Button(self, text="Enter", command=self.enterButton)

            self.inputField.grid(row=0,column=4,padx=5)
            self.inputButton.grid(row=0,column=5,padx=5)

            self.optionBar.config(state=DISABLED)


    def enterButton(self):
        value = self.inputField.get()

        if value != "" and value != "new name":
            self.cube.name = value
            self.promena.set(value)

            self.optionBar.config(state=ACTIVE)
            self.inputButton.destroy()
            self.inputField.destroy()

            self.cube.mainProgram.namePairs[self.cube.serialNumber] = value


