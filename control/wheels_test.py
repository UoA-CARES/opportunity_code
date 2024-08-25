import time
from xbox_controller import XboxController
from wheels import Wheels


def main():

    max_angular_velocity = 200
    max_linear_velocity = 500

    wheels = Wheels(
        max_linear_velocity=max_linear_velocity,
        max_angular_velocity=max_angular_velocity,
    )

    joy = XboxController()

    emergency_stop = True

    while True:

        control_inputs = joy.read()

        left_joy_x, right_trigger, left_trigger, A_button = control_inputs
        left_joy_x = round(left_joy_x, 1)

        # A button is used for emergency stopping. Can be toggled
        if A_button > 0:
            emergency_stop = not emergency_stop

        # Sending Commands to Wheels
        if emergency_stop == False:
            wheels.handle_input(
                right_trigger, left_trigger, left_joy_x
            )
        else:
            wheels.stop()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
