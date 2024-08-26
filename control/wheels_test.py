import time
from xbox_controller import XboxController
from wheels import Wheels
from util import handle_operating_mode, OperatingMode

def main():

    max_angular_velocity = 200
    max_linear_velocity = 500

    wheels = Wheels(
        max_linear_velocity=max_linear_velocity,
        max_angular_velocity=max_angular_velocity,
    )

    joy = XboxController()

    while True:

        control_inputs = joy.read()

        operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        # Sending Commands to Wheels
        if operating_mode == OperatingMode.DRIVE:
            wheels.handle_input(
                *control_inputs["wheels"]
            )
        else:
            wheels.stop()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
