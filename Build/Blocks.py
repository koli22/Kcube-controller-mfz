import threading
import tkinter
from tkinter import ttk, StringVar, OptionMenu
from tkinter.constants import DISABLED
from tkinter.constants import ACTIVE
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import tkinter.font


"""
Stores more complex UI elements
used in App.py
"""

class LayerItemCal(tkinter.Frame):
    def __init__(self, parent, image_path, myCube):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.cube = myCube

        text = self.cube.name

        # Text Label
        tkinter.Label(self, text=text,font=CUSTUM_FONT).grid(row=0, column=0, sticky="w")

        # Image (Placeholder for an image)
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image,font=CUSTUM_FONT).grid(row=0, column=1, padx=10)

        # Button
        self.button1 = tkinter.Button(self, text="Calibrate", command=self.button_action,font=CUSTUM_FONT)
        self.button1.grid(row=0, column=2, padx=5)

    def button_action(self):
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)
        self.entry = tkinter.Entry(self,font=CUSTUM_FONT)
        self.entry.grid(row=0, column=3)

        self.button2 = tkinter.Button(self, text="Enter", command=self.button_action2,font=CUSTUM_FONT)
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
            layer = LayerItemCal(self.scrollable_frame,myCube=self.cubesList[i], image_path="cube.png")
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
            layer = LayerItemInit(self.scrollable_frame,myCube=self.cubesList[i], image_path="cube.png")
            layer.pack(fill="x", pady=5)


class LayerItemInit(tkinter.Frame):
    def __init__(self, parent, image_path, myCube):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.cube = myCube

        self.serNum=tkinter.Label(self, text=self.cube.serialNumber,font=CUSTUM_FONT)
        self.serNum.grid(row=0, column=1, sticky="w", padx = 10)

        self.myName=tkinter.Label(self, text="Old name: " + str(self.cube.oldName),font=CUSTUM_FONT)
        self.myName.grid(row=0, column=2, sticky="w", padx = 10)

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
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        if (value == "new name"):
            self.inputField = tkinter.Entry(self,font=CUSTUM_FONT)
            self.inputButton = tkinter.Button(self, text="Enter", command=self.enterButton,font=CUSTUM_FONT)

            self.inputField.grid(row=0,column=4,padx=5)
            self.inputButton.grid(row=0,column=5,padx=5)

            self.optionBar.config(state=DISABLED)


    def enterButton(self):
        value = self.inputField.get()

        if value != "" and value != "new name":
            self.cube.name = value
            self.cube.oldName = value
            self.promena.set(value)

            self.optionBar.config(state=ACTIVE)
            self.inputButton.destroy()
            self.inputField.destroy()

            self.cube.mainProgram.namePairs[self.cube.serialNumber] = [value, self.cube.myType]


class ScrollableLayerListSettings(tkinter.Frame):
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
            layer = LayerItemSetting(self.scrollable_frame,myCube=self.cubesList[i], image_path="cube.png", options= self.mw.options)
            layer.pack(fill="x", pady=5)


class LayerItemSetting(tkinter.Frame):
    def __init__(self, parent, image_path, myCube, options):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.options = options

        self.cube = myCube

        self.serNum=tkinter.Label(self, text=self.cube.serialNumber,font=CUSTUM_FONT)
        self.serNum.grid(row=0, column=1, sticky="w", padx = 10)

        self.myName=tkinter.Label(self, text="Old name: " + str(self.cube.oldName),font=CUSTUM_FONT)
        self.myName.grid(row=0, column=2, sticky="w", padx = 10)

        # Image (Placeholder for an image)
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=0, padx=10)

        self.promena = StringVar(self)
        self.promena.set(self.cube.oldName)

        PARAMETRY = self.cube.allNames

        self.promena2 = StringVar(self)
        self.promena2.set(str(options[self.cube.myType]))

        self.typeSerrings = OptionMenu(self,self.promena2,*options,command=self.pumpOrProbe)
        self.typeSerrings.grid(row=0, column=3, padx=10)

        self.optionBar = OptionMenu(self,self.promena,*PARAMETRY,command=self.changeName)
        self.optionBar.grid(row=0, column=4, padx=10)



    def changeName(self,value):
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)
        self.promena.set(value)
        self.cube.changeName(value)

        if (value == "new name"):
            self.inputField = tkinter.Entry(self,font=CUSTUM_FONT)
            self.inputButton = tkinter.Button(self, text="Enter", command=self.enterButton,font=CUSTUM_FONT)

            self.inputField.grid(row=0,column=5,padx=5)
            self.inputButton.grid(row=0,column=6,padx=5)

            self.optionBar.config(state=DISABLED)


    def enterButton(self):
        value = self.inputField.get()

        if value != "" and value != "new name":
            self.cube.name = value
            self.cube.oldName = value
            self.promena.set(value)

            self.optionBar.config(state=ACTIVE)
            self.inputButton.destroy()
            self.inputField.destroy()

            self.cube.mainProgram.namePairs[self.cube.serialNumber] = [value, self.cube.myType]

    def pumpOrProbe(self, value):
        self.promena2 = str(value)
        self.cube.myType = self.options.index(value)
        self.cube.mainProgram.namePairs[self.cube.serialNumber] = [self.cube.name, self.cube.myType]

NONE_OPTION = "None"  # Represents unselected/default

# Shared manager to track global selections
class SharedOptionManager:
    def __init__(self, options):
        self.all_options = options
        self.used = {}  # { (line_id, index): option }
        self.subscribers = []

    def register(self, line):
        self.subscribers.append(line)

    def select(self, line_id, index, value):
        # Remove previous selection
        self.used = {k: v for k, v in self.used.items() if k != (line_id, index)}
        if value:
            self.used[(line_id, index)] = value
        self.update_all()

    def get_available(self, current_selection=None):
        used_values = set(v for v in self.used.values() if v != "None")
        return ["None"] + [
            opt for opt in self.all_options
            if opt not in used_values or opt == current_selection
        ]

    def update_all(self):
        for line in self.subscribers:
            line.refresh_dropdowns()

# Reusable dynamic option line widget
class OptionLine(tkinter.Frame):
    def __init__(self, parent, line_id, option_manager: SharedOptionManager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.line_id = line_id
        self.manager = option_manager
        self.manager.register(self)

        self.canvas = tkinter.Canvas(self, height=100)
        self.canvas.pack(NONE_OPTION = "None")  # Represents unselected/default

class SharedOptionManager:
    def __init__(self, options):
        self.all_options = options
        self.used = {}  # {(line_id, index): value}
        self.subscribers = []

    def register(self, line):
        self.subscribers.append(line)

    def select(self, line_id, index, value):
        # Remove previous selection
        self.used = {k: v for k, v in self.used.items() if k != (line_id, index)}
        # Do not track NONE_OPTION as used
        if value != NONE_OPTION:
            self.used[(line_id, index)] = value
        self.update_all()

    def get_available(self, current_selection=None):
        used_values = set(v for v in self.used.values() if v != NONE_OPTION)
        return [opt for opt in self.all_options if opt not in used_values or opt == current_selection]

    def update_all(self):
        for line in self.subscribers:
            line.refresh_dropdowns()


class OptionLine(tkinter.Frame):
    def __init__(self, parent, line_id, option_manager: SharedOptionManager, previous_values=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.line_id = line_id
        self.manager = option_manager
        self.manager.register(self)

        self.canvas = tkinter.Canvas(self, height=100)
        self.canvas.pack(fill="both", expand=True)

        self.frame = tkinter.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.options = []
        self.restored_values = previous_values or []
        self._restore_options()

    def _restore_options(self):
        for val in self.restored_values:
            available = self.manager.get_available()
            if val != NONE_OPTION and val not in available:
                break
            self.add_option(preselected=val)

            # Find the index of the newly added option
            index = len(self.options) - 1

            # Inform manager that this option is selected
            if val != NONE_OPTION:
                self.manager.select(self.line_id, index, val)

        self.add_option()  # always append one empty dropdown

    def add_option(self, preselected=NONE_OPTION):
        if (len(self.options) >= 3):
            return

        index = len(self.options)

        container = tkinter.Frame(self.frame, padx=10)
        container.pack(side="left")

        toggle_button = ttk.Button(container, text="Disable", command=lambda: self.toggle(index))
        toggle_button.pack(pady = 5)

        var = tkinter.StringVar()
        var.set(value=preselected)

        dropdown = ttk.Combobox(
            container,
            textvariable=var,
            values=[NONE_OPTION] + self.manager.get_available(preselected),
            state="readonly"
        )
        dropdown.pack(pady = 5)
        dropdown.bind("<<ComboboxSelected>>", lambda e, idx=index: self.on_select(idx))

        self.options.append({
            "frame": container,
            "button": toggle_button,
            "combobox": dropdown,
            "var": var,
            "enabled": True
        })


    def toggle(self, index):
        opt = self.options[index]
        opt["enabled"] = not opt["enabled"]
        new_text = "Enable" if not opt["enabled"] else "Disable"
        opt["button"].config(text=new_text)
        state = "readonly" if opt["enabled"] else "disabled"
        opt["combobox"].config(state=state)

    def on_select(self, index):
        value = self.options[index]["var"].get()
        self.manager.select(self.line_id, index, value)

        if index == len(self.options) - 1 and value != NONE_OPTION:
            self.add_option()

        # Check if last two are NONE_OPTION → remove last
        if len(self.options) >= 2:
            last_val = self.options[-1]["var"].get()
            second_last_val = self.options[-2]["var"].get()
            if last_val == NONE_OPTION and second_last_val == NONE_OPTION:
                self._remove_last_option()

    def _remove_last_option(self):
        last = self.options.pop()
        last["frame"].destroy()
        self.manager.select(self.line_id, len(self.options), NONE_OPTION)

    def refresh_dropdowns(self):
        for idx, opt in enumerate(self.options):
            current_val = opt["var"].get()
            new_values = [NONE_OPTION] + self.manager.get_available(current_val)
            opt["combobox"]["values"] = new_values

    def get_selected_values(self):
        selected = []
        for opt in self.options:
            val = opt["var"].get()
            if val != NONE_OPTION and val != "":
                selected.append(val)
        return selected

class ScrollableLayerListMainWindow(tkinter.Frame):
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
            layer = LayerItemMainWindow(self.scrollable_frame,myCube=self.cubesList[i], image_path="cube.png", options= self.mw.options)
            layer.pack(fill="x", pady=5)


class LayerItemMainWindow(tkinter.Frame):
    def __init__(self, parent, image_path, myCube, options):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.options = options

        self.cube = myCube

        self.serNum=tkinter.Label(self, text=self.cube.serialNumber,font=CUSTUM_FONT)
        self.serNum.grid(row=0, column=1, sticky="w",padx=10)

        self.myName=tkinter.Label(self, text=str(self.cube.name),font=CUSTUM_FONT)
        self.myName.grid(row=0, column=2, sticky="w",padx=10)

        # Image (Placeholder for an image)
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=0, padx=10)

        self.findButton = tkinter.Button(self, text="Find Device", command=self.findDevice,font=CUSTUM_FONT)
        self.findButton.grid(row=0, column=3,padx=10)

        self.findButton = tkinter.Button(self, text="Home Device", command=self.homeDevice,font=CUSTUM_FONT)
        self.findButton.grid(row=0, column=4,padx=10)

    def findDevice(self):
        thread = threading.Thread(target=self.cube.findDevice)
        thread.start()

    def homeDevice(self):
        thread = threading.Thread(target=self.cube.Home()) # for some reason this thread doesnt work and acts like main program
        thread.start()

