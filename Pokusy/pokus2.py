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
from System import Math



def get_all_connected_cubes():
    DeviceManagerCLI.BuildDeviceList()
    serial_numbers = DeviceManagerCLI.GetDeviceList()

    if not serial_numbers:
        raise ValueError("no cube connected")

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

def initializeConnection(controller, serialNum):
    if (controller == None):
        raise ValueError("no controller")

    controller.Connect(serialNum)
    controller.WaitForSettingsInitialized(3000)

    controller.StartPolling(50)
    time.sleep(.1)
    controller.EnableDevice()
    time.sleep(.1)
    config = controller.LoadMotorConfiguration(serialNum,
                                               DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings)
    config.DeviceSettingsName = str('PRM1-Z8')
    config.UpdateCurrentConfiguration()

def homeMotor(controller):
    print('Homing Motor')
    controller.Home(60000)


def main():
    numbers = get_all_connected_cubes()
    myNumber = numbers[0]

    DeviceManagerCLI.BuildDeviceList()
    controller = KCubeDCServo.CreateKCubeDCServo(myNumber)

    initializeConnection(controller, myNumber)
    homeMotor(controller)

    move_to_position(controller, 12, tolerance = 0.05)


    controller.StopPolling()
    controller.Disconnect(False)



def move_to_position(controller, target_position, velocity=10, step_size=10, timeout=60000, tolerance=5, max_angle=360):
    """
    Moves the motor to a specific target position using the shortest angular path (if applicable).
    """
    target_position = Decimal(target_position) % Decimal(max_angle)
    tolerance = Decimal(tolerance)
    max_angle = Decimal(max_angle)

    current_position = controller.get_Position() % max_angle
    print(f"Current Position: {current_position}")

    if Math.Abs(current_position - target_position) <= tolerance:
        print(f"Motor is already within the target proximity: {current_position}")
        return

    # Compute shortest direction (clockwise or counter-clockwise)
    clockwise_distance = (target_position - current_position + max_angle) % max_angle
    counter_clockwise_distance = (current_position - target_position + max_angle) % max_angle

    dir = 0

    if clockwise_distance <= counter_clockwise_distance:
        direction = MotorDirection.Forward
        print(f"Moving FORWARD {clockwise_distance} units")
        dir = clockwise_distance
    else:
        direction = MotorDirection.Backward
        print(f"Moving BACKWARD {counter_clockwise_distance} units")
        dir = counter_clockwise_distance


    # Set jog parameters
    jog_params = controller.GetJogParams()
    jog_params.StepSize = dir
    jog_params.VelocityParams.MaxVelocity = Decimal(velocity)
    controller.SetJogParams(jog_params)

    # Begin jog loop
    while True:
        controller.MoveJog(direction, timeout)
        time.sleep(1)
        current_position = controller.get_Position() % max_angle
        print(f"Current Position: {current_position}")

        if Math.Abs(current_position - target_position) <= tolerance:
            print(f"Target position reached (within tolerance): {current_position}")
            break

        # Compute shortest direction (clockwise or counter-clockwise)
        clockwise_distance = (target_position - current_position + max_angle) % max_angle
        counter_clockwise_distance = (current_position - target_position + max_angle) % max_angle

        dir = 0

        if clockwise_distance <= counter_clockwise_distance:
            direction = MotorDirection.Forward
            print(f"Moving FORWARD {clockwise_distance} units")
            dir = clockwise_distance
        else:
            direction = MotorDirection.Backward
            print(f"Moving BACKWARD {counter_clockwise_distance} units")
            dir = counter_clockwise_distance
        jog_params.StepSize = dir
        controller.SetJogParams(jog_params)

    print(f"Motor stopped at position: {current_position}")


def main1():
    serial_num = str('27264107')

    DeviceManagerCLI.BuildDeviceList()
    controller = KCubeDCServo.CreateKCubeDCServo(serial_num)

    if not controller == None:
        controller.Connect(serial_num)
        if not controller.IsSettingsInitialized():
            controller.WaitForSettingsInitialized(3000)

        controller.StartPolling(50)
        time.sleep(.1)
        controller.EnableDevice()
        time.sleep(.1)
        config = controller.LoadMotorConfiguration(serial_num,
                                                   DeviceConfiguration.DeviceSettingsUseOptionType.UseDeviceSettings)
        config.DeviceSettingsName = str('PRM1-Z8')
        config.UpdateCurrentConfiguration()

        print('Homing Motor')
        controller.Home(60000)

        jog_params = controller.GetJogParams()
        jog_params.StepSize = Decimal(10)
        jog_params.VelocityParams.MaxVelocity = Decimal(10)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep

        controller.SetJogParams(jog_params)

        print("Moving motor")

        #controller.MoveJog(MotorDirection.Forward, 60000)

        controller.StopPolling()
        controller.Disconnect(False)


if __name__ == "__main__":
    main()