import time
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.DCServoCLI.dll")


from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal

import os


def list_connected_kcubes():
    """
    This function builds the device list and returns the serial numbers of all connected K-Cubes.
    """
    # Build the device list
    DeviceManagerCLI.BuildDeviceList()

    # Get all connected device serial numbers (as strings)
    serial_numbers = DeviceManagerCLI.GetDeviceList()

    if not serial_numbers:
        print("No K-Cubes detected.")
        return []

    connected_kcubes = []

    for serial in serial_numbers:
        try:
            # Try creating a KCubeDCServo with the serial number
            device = KCubeDCServo.CreateKCubeDCServo(serial)
            if device is not None:
                connected_kcubes.append(serial)
        except Exception:
            pass

    return connected_kcubes


def main():
    # List all connected K-Cubes
    kcubes = list_connected_kcubes()

    if kcubes:
        print(f"Connected K-Cubes: {kcubes}")
    else:
        print("No K-Cubes are connected.")


if __name__ == "__main__":
    main()