# Importing .NET Common Language Runtime (CLR) for accessing C# libraries

import clr
import time

# Adding references to Thorlabs Kinesis .NET assemblies

path = "C:\\Program Files\\Thorlabs\\Kinesis\\"

clr.AddReference(path + "Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference(path + "Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference(path + "ThorLabs.MotionControl.KCube.DCServoCLI.dll")

# Importing specific modules from the Kinesis libraries

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal
from System import Math


class Cube:
    """
    Class for managing and controlling a Thorlabs KCube motor device.
    """

    def __init__(self, program):
        # Initialization of Cube attributes
        self.name = "unnamed"  # Device name
        self.serialNumber = "-1"  # Serial number placeholder
        self.offset = Decimal(0)  # Mechanical offset in degrees
        self.controller = None  # Will hold the device controller object
        self.invrted = False  # Flag to indicate if motor direction is inverted
        self.oldName = ""  # Stores the name attached to this serial number last time
        self.allNames = [] # List of all names stored last time
        self.mainProgram = program  # reference to root program
        self.myType = 0             # probe/pump
        self.dc = DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings     # configuration

    def addName(self, name):                    # add name to the list of all names
        if (self.allNames.count(name) == 0):
            self.allNames.append(str(name))

    def initializeCube(self):
        # Detects and connects to the motor controller
        DeviceManagerCLI.BuildDeviceList()

        if (self.serialNumber == "-1"):
            raise ReferenceError("no serial number")

        print(self.serialNumber)

        # Create and connect the KCube DC Servo controller
        self.controller = KCubeDCServo.CreateKCubeDCServo(self.serialNumber)
        self.controller.Connect(self.serialNumber)
        self.controller.WaitForSettingsInitialized(3000)

        self.controller.StartPolling(50)  # Begin polling the device for status
        time.sleep(.1)
        self.controller.EnableDevice()  # Enable the motor
        time.sleep(.1)

        # Load and update motor configuration
        config = self.controller.LoadMotorConfiguration(
            self.serialNumber,
            DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings
        )
        config.DeviceSettingsName = str('PRM1-Z8')
        config.UpdateCurrentConfiguration()

        # Home the motor and check direction
        self.controller.Home(60000)
        self.detectIfInverted()

    def changeName(self, newName):      # change devices name
        if (self.name != newName):
            self.name = newName

    def setSerialNumber(self, newNumber):
        # Set the serial number only once
        if (self.serialNumber == "-1"):
            self.serialNumber = newNumber
        else:
            raise ValueError("serial number already set")

    def setOffset(self, newOffset):
        offsetAngle = self.controller.get_Position() - Decimal(newOffset)

        # Normalize and store offset angle
        offsetAngle = self.normalizeAngle(offsetAngle)
        self.offset = offsetAngle

        print("new offset", self.offset)

    def normalizeAngle(self, angle):
        # Normalize angle to range 0–359
        normalizedAngle = angle % Decimal(360)
        while normalizedAngle < Decimal(0):
            normalizedAngle += Decimal(360)

        return normalizedAngle

    def Home(self):
        # Home the motor and move to logical zero
        print('Homing Motor')
        self.controller.Home(60000)
        self.move_to_position(0, tolerance=0)


    # Not in use

    def move_to_position2(self, target_position, velocity=10, timeout=60000, tolerance=5, max_angle=360):
        """
        Moves motor to a target angle in range (0, 360).
        Applies mechanical offset and handles inversion logic.
        """

        target_position = (Decimal(target_position) + self.offset) % Decimal(max_angle)
        tolerance = Decimal(tolerance)
        max_angle = Decimal(max_angle)

        current_position = self.controller.get_Position() % max_angle
        print(f"Current Position: {current_position - self.offset}")

        if Math.Abs(current_position - target_position) <= tolerance:
            print(f"Motor is already within the target proximity: {current_position - self.offset}")
            return

        while True:
            if (current_position > target_position):
                direction = MotorDirection.Backward
            else:
                direction = MotorDirection.Forward


            if (self.invrted and direction == MotorDirection.Forward):
                direction = MotorDirection.Backward
            elif (self.invrted and direction == MotorDirection.Backward):
                direction = MotorDirection.Forward

            ditsance = Math.Abs(current_position - target_position)

            jog_params = self.controller.GetJogParams()
            jog_params.StepSize = ditsance
            jog_params.VelocityParams.MaxVelocity = Decimal(velocity)
            self.controller.SetJogParams(jog_params)

            self.controller.MoveJog(direction, timeout)
            time.sleep(1)

            if Math.Abs(current_position - target_position) <= tolerance:
                print(f"Reached position: {current_position - self.offset}")
                return


    def move_to_position(self, target_position, velocity=10, timeout=60000, tolerance=0, max_angle=360):
        """
        Moves motor to a target angle with shortest angular distance.
        Applies mechanical offset and handles inversion logic.
        """


        # convert values to C# System.Decimal
        target_position = (Decimal(target_position) + self.offset) % Decimal(max_angle)
        tolerance = Decimal(tolerance)
        max_angle = Decimal(max_angle)

        current_position = self.controller.get_Position() % max_angle
        print(f"Current Position: {current_position - self.offset}")

        if Math.Abs(current_position - target_position) <= tolerance:
            print(f"Motor is already within the target proximity: {current_position - self.offset}")
            return

        # Compute shortest direction (clockwise or counter-clockwise)
        clockwise_distance = (target_position - current_position + max_angle) % max_angle
        counter_clockwise_distance = (current_position - target_position + max_angle) % max_angle

        dir = 0

        if (clockwise_distance <= counter_clockwise_distance):
            direction = MotorDirection.Forward
            print(f"Moving FORWARD {clockwise_distance} units")
            dir = clockwise_distance
        else:
            direction = MotorDirection.Backward
            print(f"Moving BACKWARD {counter_clockwise_distance} units")
            dir = counter_clockwise_distance

        if (self.invrted and direction == MotorDirection.Forward):
            direction = MotorDirection.Backward
        elif (self.invrted and direction == MotorDirection.Backward):
            direction = MotorDirection.Forward

        # Set jog parameters
        jog_params = self.controller.GetJogParams()
        jog_params.StepSize = dir
        jog_params.VelocityParams.MaxVelocity = Decimal(velocity)
        self.controller.SetJogParams(jog_params)

        # Begin jog loop
        while True:
            self.controller.MoveJog(direction, timeout)
            time.sleep(1)
            current_position = self.controller.get_Position() % max_angle
            print(f"Current Position: {current_position - self.offset}")

            if Math.Abs(current_position - target_position) <= tolerance:
                print(f"Target position reached (within tolerance): {current_position - self.offset}")
                break

            # Compute shortest direction (clockwise or counter-clockwise)
            clockwise_distance = (target_position - current_position + max_angle) % max_angle
            counter_clockwise_distance = (current_position - target_position + max_angle) % max_angle

            dir = 0

            if (clockwise_distance <= counter_clockwise_distance):
                direction = MotorDirection.Forward
                print(f"Moving FORWARD {clockwise_distance} units")
                dir = clockwise_distance
            else:
                direction = MotorDirection.Backward
                print(f"Moving BACKWARD {counter_clockwise_distance} units")
                dir = counter_clockwise_distance

            if (self.invrted and direction == MotorDirection.Forward):
                direction = MotorDirection.Backward
            elif (self.invrted and direction == MotorDirection.Backward):
                direction = MotorDirection.Forward

            jog_params.StepSize = dir
            self.controller.SetJogParams(jog_params)

        print(f"Motor stopped at position: {current_position - self.offset}")

    def detectIfInverted(self, max_angle=360, velocity=10, step=10, timeout=60000):
        """
        Moves motor forward and checks if position decreases.
        If yes, motor direction is inverted.
        """

        step = Decimal(step)

        max_angle = Decimal(max_angle)

        currentPosition = self.controller.get_Position()

        print(currentPosition)

        jog_params = self.controller.GetJogParams()
        jog_params.StepSize = step
        jog_params.VelocityParams.MaxVelocity = Decimal(velocity)
        self.controller.SetJogParams(jog_params)

        self.controller.MoveJog(MotorDirection.Forward, timeout)

        newPosition = self.controller.get_Position()
        print(newPosition)
        if (currentPosition > Decimal(340)):
            currentPosition -= Decimal(360)

        print(currentPosition)

        if (currentPosition > newPosition):
            self.invrted = True

            print("Inverted")

        self.Home()

    def disconnect(self):
        if self.controller == None:  # no connection
            return

        # Stop polling and safely disconnect device
        self.controller.StopPolling()
        self.controller.Disconnect(False)

        print("disconnected " + self.serialNumber)

    def getCurrentPosition(self):
        return self.controller.get_Position()

    def findDevice(self):
        self.move_to_position(5, tolerance=1, velocity=30, timeout=10000)
        self.move_to_position(0, tolerance=1, velocity=30, timeout=10000)

    def give_offset(self):
        return (Decimal(360) - self.offset) % Decimal(360)