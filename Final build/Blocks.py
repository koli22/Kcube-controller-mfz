# Importing required libraries
import threading
import tkinter
from tkinter import ttk, StringVar, OptionMenu
from tkinter.constants import DISABLED, ACTIVE
from PIL import Image, ImageTk
import tkinter.font

"""
Stores more complex UI elements
used in App.py.
"""


class LayerItemCal(tkinter.Frame):  # Calibration layer. Stores all the UI elements.
    def __init__(self, parent, image_path, myCube):  # Manages layout, image, buttons, and interaction.
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")
        CUSTOM_FONT = tkinter.font.Font(family="Arial", size=10)  # Define custom font.

        self.cube = myCube  # Store cube object assigned to this layer.

        text = str(self.cube.name)  # Text for label 1.
        text2 = str(self.cube.serialNumber)  # Text for label 2.

        tkinter.Label(self, text=text, font=CUSTOM_FONT).grid(row=0, column=1, sticky="w", padx=10)
        tkinter.Label(self, text=text2, font=CUSTOM_FONT).grid(row=0, column=2, sticky="w", padx=10)

        # Label showing the current offset; can be updated later.
        self.offtext = tkinter.Label(self, text=("Current set offset: " + str(self.cube.give_offset())),
                                     font=CUSTOM_FONT)
        self.offtext.grid(row=0, column=3, sticky="w", padx=10)

        # Load and resize image
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image, font=CUSTOM_FONT).grid(row=0, column=0, padx=10)

        # Create button to start calibration
        self.button1 = tkinter.Button(self, text="Calibrate", command=self.button_action, font=CUSTOM_FONT)
        self.button1.grid(row=0, column=4, padx=5)

    def button_action(self):  # Callback when "Calibrate" button is clicked.
        CUSTOM_FONT = tkinter.font.Font(family="Arial", size=10)

        # Create entry widget for offset input
        self.entry = tkinter.Entry(self, font=CUSTOM_FONT)
        self.entry.grid(row=0, column=5)

        # Create button to confirm the calibration
        self.button2 = tkinter.Button(self, text="Enter", command=self.button_action2, font=CUSTOM_FONT)
        self.button2.grid(row=0, column=6, padx=5)

        self.button1.config(state=DISABLED)  # Disable the first button during input

    def button_action2(self):  # Confirm calibration
        _input = self.entry.get()
        number = -1

        if _input == "":  # Check if input is empty
            print("empty")
            self.button1.config(state=ACTIVE)
            self.button2.destroy()
            self.entry.destroy()
            return

        try:
            _input = int(_input)  # Convert input to int
            if 0 <= _input < 360:
                number = _input
        except:
            pass  # Ignore invalid input

        if number >= 0:  # Valid offset
            self.button1.config(state=ACTIVE)
            self.button2.destroy()
            self.entry.destroy()

            self.cube.setOffset(number)  # Set the offset on the cube

            # Create and start a thread to run cube.Home()
            thread = threading.Thread(target=self.cube.Home)
            thread.start()

            # Update UI while the thread is running
            running = True
            while running:
                running = thread.is_alive()
                self.cube.mainProgram.parent.update()

            try:
                CUSTOM_FONT = tkinter.font.Font(family="Arial", size=10)
                self.offtext = tkinter.Label(self, text=("Current set offset: " + str(self.cube.give_offset())),
                                             font=CUSTOM_FONT)
                self.cube.mainProgram.checkPopup(self, self.cube.offset)
            except:
                pass


# A scrollable frame for calibration layer items
class ScrollableLayerListCal(tkinter.Frame):
    def __init__(self, parent, mw):
        super().__init__(parent)

        self.cubesList = mw.cubes  # List of cube objects
        self.mw = mw  # Reference to main window

        # Create scrollable canvas
        canvas = tkinter.Canvas(self, width=500, height=300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas)

        # Automatically adjust scrollable region when the frame is resized
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Place the inner frame inside the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add a LayerItemCal widget for each cube
        for i in range(len(self.cubesList)):
            layer = LayerItemCal(self.scrollable_frame, myCube=self.cubesList[i], image_path="cube.png")
            layer.pack(fill="x", pady=5)


# A scrollable frame for initialization layer items
class ScrollableLayerListInit(tkinter.Frame):
    def __init__(self, parent, mw):
        super().__init__(parent)

        self.cubesList = mw.cubes  # List of cube objects
        self.mw = mw  # Reference to main window

        # Create scrollable canvas
        canvas = tkinter.Canvas(self, width=500, height=300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas)

        # Automatically adjust scrollable region when the frame is resized
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Place the inner frame inside the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add a LayerItemInit widget for each cube
        for i in range(len(self.cubesList)):
            layer = LayerItemInit(self.scrollable_frame, myCube=self.cubesList[i], image_path="cube.png")
            layer.pack(fill="x", pady=5)


# A frame representing a single cube for name initialization
class LayerItemInit(tkinter.Frame):
    def __init__(self, parent, image_path, myCube):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.cube = myCube  # Cube object assigned to this layer

        # Serial number label
        self.serNum = tkinter.Label(self, text=self.cube.serialNumber, font=CUSTUM_FONT)
        self.serNum.grid(row=0, column=1, sticky="w", padx=10)

        # Old name label
        self.myName = tkinter.Label(self, text="Old name: " + str(self.cube.oldName), font=CUSTUM_FONT)
        self.myName.grid(row=0, column=2, sticky="w", padx=10)

        # Cube image
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=0, padx=10)

        # Dropdown for selecting a name
        self.promena = StringVar(self)
        self.promena.set(self.cube.oldName)
        PARAMETRY = self.cube.allNames
        self.optionBar = OptionMenu(self, self.promena, *PARAMETRY, command=self.changeName)
        self.optionBar.grid(row=0, column=3, padx=5)

    # Handle name change or switch to custom name input
    def changeName(self, value):
        self.promena.set(value)
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        if value == "new name":
            self.inputField = tkinter.Entry(self, font=CUSTUM_FONT)
            self.inputButton = tkinter.Button(self, text="Enter", command=self.enterButton, font=CUSTUM_FONT)

            self.inputField.grid(row=0, column=4, padx=5)
            self.inputButton.grid(row=0, column=5, padx=5)

            self.optionBar.config(state=DISABLED)
        else:
            self.cube.changeName(value)

    # Confirm entry of a new custom name
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
        elif value == "":
            self.promena.set(self.cube.oldName)
            self.optionBar.config(state=ACTIVE)
            self.inputButton.destroy()
            self.inputField.destroy()


# Scrollable list for initialization layer items
class ScrollableLayerListSettings(tkinter.Frame):
    def __init__(self, parent, mw):
        super().__init__(parent)

        self.cubesList = mw.cubes  # List of cubes
        self.mw = mw  # Reference to main window

        # Create scrollable canvas
        canvas = tkinter.Canvas(self, width=500, height=300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tkinter.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add a LayerItemSetting widget for each cube
        for i in range(len(self.cubesList)):
            layer = LayerItemSetting(self.scrollable_frame, myCube=self.cubesList[i], image_path="cube.png", options=self.mw.options)
            layer.pack(fill="x", pady=5)

# A single UI component for displaying and editing cube settings (name and type)
class LayerItemSetting(tkinter.Frame):
    def __init__(self, parent, image_path, myCube, options):
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.options = options      # List of type options (e.g., Pump, Probe, etc.)
        self.cube = myCube          # The cube object this item represents

        # Display cube's serial number
        self.serNum = tkinter.Label(self, text=self.cube.serialNumber, font=CUSTUM_FONT)
        self.serNum.grid(row=0, column=1, sticky="w", padx=10)

        # Display current name
        self.myName = tkinter.Label(self, text="Old name: " + str(self.cube.oldName), font=CUSTUM_FONT)
        self.myName.grid(row=0, column=2, sticky="w", padx=10)

        # Show image representation of cube
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=0, padx=10)

        # Name dropdown initialization
        self.promena = StringVar(self)
        self.promena.set(self.cube.oldName)
        PARAMETRY = self.cube.allNames

        self.optionBar = OptionMenu(self, self.promena, *PARAMETRY, command=self.changeName)
        self.optionBar.grid(row=0, column=4, padx=10)

        # Type dropdown initialization
        self.promena2 = StringVar(self)
        self.promena2.set(str(options[self.cube.myType]))  # Default selected type
        self.typeSerrings = OptionMenu(self, self.promena2, *options, command=self.pumpOrProbe)
        self.typeSerrings.grid(row=0, column=3, padx=10)

    # Callback when a name is selected or "new name" is chosen
    def changeName(self, value):
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)
        self.promena.set(value)

        if value == "new name":
            # Allow manual input of a custom name
            self.inputField = tkinter.Entry(self, font=CUSTUM_FONT)
            self.inputButton = tkinter.Button(self, text="Enter", command=self.enterButton, font=CUSTUM_FONT)

            self.inputField.grid(row=0, column=5, padx=5)
            self.inputButton.grid(row=0, column=6, padx=5)

            self.optionBar.config(state=DISABLED)
        else:
            self.cube.changeName(value)

    # Handle manual name entry and update cube data
    def enterButton(self):
        value = self.inputField.get()

        if value != "" and value != "new name":
            self.cube.name = value
            self.cube.oldName = value
            self.promena.set(value)

            self.optionBar.config(state=ACTIVE)
            self.inputButton.destroy()
            self.inputField.destroy()

            # Update name in shared mapping
            self.cube.mainProgram.namePairs[self.cube.serialNumber] = [value, self.cube.myType]
        elif value == "":
            # If input is empty, revert to previous name
            self.promena.set(self.cube.oldName)
            self.optionBar.config(state=ACTIVE)
            self.inputButton.destroy()
            self.inputField.destroy()

    # Callback when cube type (e.g., Pump or Probe) is changed
    def pumpOrProbe(self, value):
        self.promena2 = str(value)
        self.cube.myType = self.options.index(value)

        # Update name-type mapping in main program
        self.cube.mainProgram.namePairs[self.cube.serialNumber] = [self.cube.name, self.cube.myType]


# Constant for representing unselected/default option
NONE_OPTION = "None"

# A centralized manager to coordinate dropdown selections across multiple UI components
class SharedOptionManager:
    def __init__(self, options):
        self.all_options = options  # List of all dropdown options
        self.used = {}              # Tracks used values: { (line_id, index): selected_value }
        self.subscribers = []      # All registered dropdown components

    def register(self, line):
        self.subscribers.append(line)

    # Handle when a dropdown value is selected
    def select(self, line_id, index, value):
        # Remove previous value for this (line_id, index)
        self.used = {k: v for k, v in self.used.items() if k != (line_id, index)}
        if value:
            self.used[(line_id, index)] = value
        self.update_all()

    # Return available options, excluding used ones (except the current selection)
    def get_available(self, current_selection=None):
        used_values = set(v for v in self.used.values() if v != NONE_OPTION)
        return [NONE_OPTION] + [
            opt for opt in self.all_options
            if opt not in used_values or opt == current_selection
        ]

    # Notify all registered dropdowns to refresh their option lists
    def update_all(self):
        for line in self.subscribers:
            line.refresh_dropdowns()

# Reusable dynamic option line widget
class OptionLine(tkinter.Frame):
    def __init__(self, parent, line_id, option_manager: SharedOptionManager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.line_id = line_id                      # Unique ID for this line/widget
        self.manager = option_manager               # Shared option manager instance
        self.manager.register(self)                 # Register this line with the shared manager

        # Create a canvas widget inside the frame to hold visual components
        self.canvas = tkinter.Canvas(self, height=100)
        # Pack the canvas into the frame; NOTE: Incorrect use of 'pack' here with invalid argument
        self.canvas.pack(NONE_OPTION = "None")      # NONE_OPTION should be defined elsewhere (e.g. as a global const)

# Manager class that tracks selected options across all OptionLine instances
class SharedOptionManager:
    def __init__(self, options):
        self.all_options = options                  # All possible options for selection
        self.used = {}                              # Dictionary of used values {(line_id, index): value}
        self.subscribers = []                       # List of OptionLine instances to update on change

    def register(self, line):
        # Add a new OptionLine to the list of subscribers
        self.subscribers.append(line)

    def select(self, line_id, index, value):
        # Remove the previous selection for the given (line_id, index)
        self.used = {k: v for k, v in self.used.items() if k != (line_id, index)}
        # Only add to 'used' if the selected value is not the placeholder NONE_OPTION
        if value != NONE_OPTION:
            self.used[(line_id, index)] = value
        # Notify all subscribers to refresh their dropdowns
        self.update_all()

    def get_available(self, current_selection=None):
        # Return options not currently selected, allowing the current selection to remain
        used_values = set(v for v in self.used.values() if v != NONE_OPTION)
        return [opt for opt in self.all_options if opt not in used_values or opt == current_selection]

    def update_all(self):
        # Call refresh method on all subscribed OptionLine instances
        for line in self.subscribers:
            line.refresh_dropdowns()


class OptionLine(tkinter.Frame):
    def __init__(self, parent, line_id, option_manager: SharedOptionManager, possibleStates: list,
                 previous_values=None, previous_states=None, prev_enabled=[True, True, True], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.line_id = line_id                        # Unique identifier for this line
        self.manager = option_manager                 # SharedOptionManager instance to handle global state
        self.manager.register(self)                   # Register this line with the shared manager

        self.possibleStates = possibleStates          # List of possible secondary state values
        self.selectedStates = [0, 0, 0]               # Currently selected secondary states for each option

        # Create and pack canvas for layout
        self.canvas = tkinter.Canvas(self, height=100)
        self.canvas.pack(fill="both", expand=True)

        # Frame inside canvas to hold widgets
        self.frame = tkinter.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.options = []                             # Stores option widget metadata
        self.restored_values = previous_values or []  # Values from previous session, if any
        self.restored_states = previous_states or []  # State values from previous session
        self.prev_enabled = prev_enabled              # Previously enabled/disabled status of dropdowns

        # Ensure restored_states has length 3
        for i in range(len(self.restored_states), 3):
            self.restored_states.append(None)

        self._restore_options()                       # Populate UI with restored data

    def _restore_options(self):
        i = 0
        for val in self.restored_values:
            available = self.manager.get_available()
            if val != NONE_OPTION and val not in available:
                break  # Skip adding if the restored value is invalid
            self.add_option(preselected=val, prestate=self.restored_states[i], enabled=self.prev_enabled[i])

            index = len(self.options) - 1  # Index of just-added option

            # Notify manager of selection
            if val != NONE_OPTION:
                self.manager.select(self.line_id, index, val)

            i += 1

        # Ensure 3 total options are always shown
        for i in range(3):
            self.add_option()

    def add_option(self, preselected=NONE_OPTION, prestate=None, enabled=True):
        if len(self.options) >= 3:
            return  # Do not exceed 3 options

        index = len(self.options)

        # Frame container for widgets in this option
        container = tkinter.Frame(self.frame, padx=10)
        container.pack(side="left")

        # Toggle enable/disable button
        toggle_button = ttk.Button(container, text="Disable", command=lambda: self.toggle(index))
        toggle_button.pack(pady=5)

        # Main dropdown variable and widget
        var = tkinter.StringVar()
        var.set(value=preselected)
        dropdown = ttk.Combobox(
            container,
            textvariable=var,
            values=[NONE_OPTION] + self.manager.get_available(preselected),
            state="readonly"
        )
        dropdown.pack(pady=5)
        dropdown.bind("<<ComboboxSelected>>", lambda e, idx=index: self.on_select(idx))

        # Secondary state dropdown variable and widget
        var2 = tkinter.StringVar()
        var2.set(value=self.possibleStates[0])
        self.selectedStates[len(self.options)] = self.possibleStates[0]

        if prestate is not None and prestate in self.possibleStates:
            var2.set(value=prestate)
            self.selectedStates[len(self.options)] = prestate

        dropdown2 = ttk.Combobox(
            container,
            textvariable=var2,
            values=self.possibleStates,
            state="readonly"
        )
        dropdown2.pack(pady=5)
        dropdown2.bind("<<ComboboxSelected>>", lambda e, idx=index: self.on_select2(idx))

        # Store all widget references and state
        self.options.append({
            "frame": container,
            "button": toggle_button,
            "combobox": dropdown,
            "states": dropdown2,
            "var": var,
            "var2": var2,
            "enabled": True
        })

        # Apply initial enabled/disabled state
        if not enabled:
            self.toggle(index)

    def on_select2(self, index):
        # Handler for secondary dropdown selection
        value = self.options[index]["var2"].get()
        self.selectedStates[index] = value

    def get_dropdown2(self):
        # Returns selected states from secondary dropdowns
        return self.selectedStates

    def get_enabled(self):
        # Returns list of booleans indicating which options are enabled
        ret_line = []
        for i in range(len(self.options)):
            ret_line.append(self.options[i]["enabled"])
        # Pad with True if fewer than 3
        for i in range(len(ret_line), 3):
            ret_line.append(True)
        return ret_line

    def toggle(self, index):
        # Toggle enable/disable for option at index
        opt = self.options[index]
        opt["enabled"] = not opt["enabled"]
        new_text = "Enable" if not opt["enabled"] else "Disable"
        opt["button"].config(text=new_text)
        state = "readonly" if opt["enabled"] else "disabled"
        opt["combobox"].config(state=state)

    def on_select(self, index):
        # Handler for primary dropdown selection
        value = self.options[index]["var"].get()
        self.manager.select(self.line_id, index, value)

        # The following logic is commented out but shows intention to dynamically add/remove options
        """
        if index == len(self.options) - 1 and value != NONE_OPTION:
            self.add_option()

        # Check if last two options are NONE_OPTION; if so, remove the last
        if len(self.options) >= 2:
            last_val = self.options[-1]["var"].get()
            second_last_val = self.options[-2]["var"].get()
            if last_val == NONE_OPTION and second_last_val == NONE_OPTION:
                self._remove_last_option()
        """

    def _remove_last_option(self):
        # Remove the most recently added option
        last = self.options.pop()
        last["frame"].destroy()
        self.manager.select(self.line_id, len(self.options), NONE_OPTION)

    def refresh_dropdowns(self):
        # Refresh available options in all primary dropdowns
        for idx, opt in enumerate(self.options):
            current_val = opt["var"].get()
            new_values = [NONE_OPTION] + self.manager.get_available(current_val)
            opt["combobox"]["values"] = new_values

    def get_selected_values(self):
        # Return list of non-empty, non-"None" selected values from primary dropdowns
        selected = []
        for opt in self.options:
            val = opt["var"].get()
            if val != NONE_OPTION and val != "":
                selected.append(val)
        return selected

class ScrollableLayerListMainWindow(tkinter.Frame):
    def __init__(self, parent, mw):
        super().__init__(parent)

        self.cubesList = mw.cubes        # List of cube objects from main window (mw)
        self.mw = mw                     # Reference to main window

        # Create a canvas widget with fixed size for scrolling content
        canvas = tkinter.Canvas(self, width=500, height=300)
        # Create a vertical scrollbar linked to the canvas y-axis view
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        # Frame inside the canvas that will contain the actual scrollable widgets
        self.scrollable_frame = tkinter.Frame(canvas)

        # When the inner frame changes size, update the canvas scroll region to fit content
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")  # Set scroll region to bounding box of all contents
            )
        )

        # Create a window inside the canvas at position (0,0) anchoring to northwest corner
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Link the scrollbar's set method to the canvas's yscrollcommand (sync scrollbar and canvas)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas on the left, expanding to fill available space
        canvas.pack(side="left", fill="both", expand=True)
        # Pack the scrollbar on the right, filling vertically
        scrollbar.pack(side="right", fill="y")

        # Populate scrollable frame with LayerItemMainWindow widgets, one for each cube
        for i in range(len(self.cubesList)):
            layer = LayerItemMainWindow(
                self.scrollable_frame,
                myCube=self.cubesList[i],
                image_path="cube.png",           # Placeholder image file path
                options=self.mw.options           # Pass options from main window
            )
            layer.pack(fill="x", pady=5)         # Pack horizontally with vertical padding


class LayerItemMainWindow(tkinter.Frame):
    def __init__(self, parent, image_path, myCube, options):
        # Initialize Frame with padding, border, and solid relief
        super().__init__(parent, pady=10, padx=10, bd=1, relief="solid")

        # Custom font for labels and buttons
        CUSTUM_FONT = tkinter.font.Font(family="Arial", size=10)

        self.options = options       # Store options passed in (purpose not shown in snippet)
        self.cube = myCube           # Store reference to the cube object

        # Label showing cube's serial number
        self.serNum = tkinter.Label(self, text=self.cube.serialNumber, font=CUSTUM_FONT)
        self.serNum.grid(row=0, column=1, sticky="w", padx=10)  # Left aligned with padding

        # Label showing cube's name
        self.myName = tkinter.Label(self, text=str(self.cube.name), font=CUSTUM_FONT)
        self.myName.grid(row=0, column=2, sticky="w", padx=10)

        # Load and resize image, then create PhotoImage for Tkinter display
        img = Image.open(image_path).resize((50, 50))
        self.tk_image = ImageTk.PhotoImage(img)
        # Place image in a Label widget at first column
        tkinter.Label(self, image=self.tk_image).grid(row=0, column=0, padx=10)

        # Button to trigger "find device" action for the cube
        self.findButton = tkinter.Button(self, text="Find Device", command=self.findDevice, font=CUSTUM_FONT)
        self.findButton.grid(row=0, column=3, padx=10)

        # Button to trigger "home device" action for the cube
        self.findButton = tkinter.Button(self, text="Home Device", command=self.homeDevice, font=CUSTUM_FONT)
        self.findButton.grid(row=0, column=4, padx=10)

    def findDevice(self):
        # Run cube.findDevice in a separate thread to avoid blocking the GUI
        thread = threading.Thread(target=self.cube.findDevice)
        thread.start()
        thread.join()  # Wait for thread to complete (could block UI; consider removing join)

    def homeDevice(self):
        # This thread creation is incorrect: self.cube.Home() is called immediately
        # Instead, pass the function itself (without parentheses) to the thread
        thread = threading.Thread(target=self.cube.Home)  # Fixed threading target
        thread.start()
        thread.join()  # Wait for thread to complete (again, can block UI)


class LayerItemText(tkinter.Frame):
    def __init__(self, parent, myText):
        # Initialize a Frame with padding and no border/relief
        super().__init__(parent, pady=10, padx=10, bd=0, relief="flat", highlightthickness=0)

        # Define a custom font for the label text
        CUSTOM_FONT = tkinter.font.Font(family="Arial", size=10)

        # Create a Label to display the (possibly trimmed) text
        # Text is left-justified, anchored west, and wrapped at 800 pixels width
        self.text = tkinter.Label(
            self,
            text=self.cutText(myText),
            font=CUSTOM_FONT,
            justify="left",
            anchor="w",
            wraplength=800
        )
        # Position label using grid, aligned left with horizontal padding
        self.text.grid(row=0, column=0, sticky="w", padx=10)

    def cutText(self, _text):
        # Placeholder to process text if needed, currently returns input unchanged
        return _text
        # Uncomment below to insert newlines every 120 chars (optional)
        # return self.insert_newlines(_text)

    def insert_newlines(self, _text, every=120):
        # Utility to insert newline characters into long text every `every` chars
        return '\n'.join(_text[i:i + every] for i in range(0, len(_text), every))


class scrollableManual(tkinter.Frame):
    def __init__(self, parent, mw, manualText):
        # Initialize main Frame container
        super().__init__(parent)

        # Create canvas widget with fixed width/height and no border highlight
        self.canvas = tkinter.Canvas(self, width=860, height=430, highlightthickness=0, bd=0)
        # Create vertical scrollbar linked to canvas yview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # Frame inside the canvas that will contain all manual text sections
        self.scrollable_frame = tkinter.Frame(self.canvas, bd=0, highlightthickness=0)
        # Place scrollable_frame inside the canvas at top-left corner
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # Connect scrollbar to canvas scroll commands
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas to fill horizontally and vertically, scrollbar on right side vertically
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # When the scrollable_frame resizes, update the scroll region accordingly
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Bind mouse wheel events to allow scrolling with mouse wheel
        self.bind_mousewheel()

        # Split manualText by newline, skipping the first empty or header line,
        # then create a LayerItemText widget for each text block, packing vertically
        for region in manualText.split("\n")[1:]:
            layer = LayerItemText(self.scrollable_frame, region)
            layer.pack(fill="x", pady=5)

    def bind_mousewheel(self):
        # Bind mouse wheel events for different platforms
        self.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows / MacOS
        self.bind_all("<Button-4>", self._on_mousewheel_linux_up)  # Linux scroll up
        self.bind_all("<Button-5>", self._on_mousewheel_linux_down)  # Linux scroll down

    def unbind_mousewheel(self):
        # Remove all mouse wheel bindings (cleanup)
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        # Scroll canvas vertically by number of units determined by wheel delta (Windows/MacOS)
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux_up(self, event):
        # Scroll canvas up by one unit (Linux)
        self.canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        # Scroll canvas down by one unit (Linux)
        self.canvas.yview_scroll(1, "units")

    def destroy(self):
        # Before destroying widget, unbind mouse wheel events to prevent errors
        self.unbind_mousewheel()
        super().destroy()
