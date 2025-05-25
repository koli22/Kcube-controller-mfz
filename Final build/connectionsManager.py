# Import CLR (Common Language Runtime) to use .NET libraries in Python
import clr
import time

# Define the path to the Thorlabs Kinesis libraries
path = "C:\\Program Files\\Thorlabs\\Kinesis\\"

# Add references to required Thorlabs Kinesis DLLs
clr.AddReference(path + "Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference(path + "Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference(path + "ThorLabs.MotionControl.KCube.DCServoCLI.dll")

# Import classes from the referenced Kinesis assemblies
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal
from System import Math


class connectionsManager:
    """
    Class responsible for managing connections to Thorlabs KCube devices.
    """

    def getAllConnectedCubes(self):
        """
        Builds the device list and returns a list of connected KCube serial numbers.
        """
        # Build the list of devices connected via USB
        DeviceManagerCLI.BuildDeviceList()
        serial_numbers = DeviceManagerCLI.GetDeviceList()  # Get list of connected device serial numbers

        if not serial_numbers:
            # If no devices found, raise an error
            #raise ValueError("no cube connected")
            pass

        connected_kcubes = []

        # Loop through each device and try to create a KCubeDCServo object
        for serial in serial_numbers:
            try:
                device = KCubeDCServo.CreateKCubeDCServo(serial)
                if device is not None:
                    connected_kcubes.append(serial)  # Add valid KCube serial to the list
            except Exception:
                # Handle devices that fail to connect
                print("couldn't connect to cube")

        return connected_kcubes  # Return list of connected and valid KCube serial numbers
