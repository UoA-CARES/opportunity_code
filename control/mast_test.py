import time
from xbox_controller import XboxController
from mast import Mast
from util import handle_operating_mode, OperatingMode

def main():

    max_angular_velocity = 200

    mast = Mast(max_angular_velocity)

    joy = XboxController()

    while True:

        control_inputs = joy.read()

        operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        # Sending Commands to Wheels
        if operating_mode == OperatingMode.DRIVE:
            mast.handle_input(
                *control_inputs["mast"]
            )
        else:
            mast.stop_rotating()
            mast.stop_tilting()

        time.sleep(0.01)


if __name__ == "__main__":
    main()