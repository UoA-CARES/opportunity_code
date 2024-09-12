
import time
from control import (
    handle_operating_mode,
    OperatingMode,
    arm,
    XboxController,
    SoundEffects,
    handle_check_mode,
    play_check_mode_sound,
)


def main():


    arm_ = arm.Arm()

    joy = XboxController()
    sounds_effects = SoundEffects()

    operating_mode = OperatingMode.STATIONARY

    while True:

        control_inputs = joy.read()

        new_operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        #Change Operating Mode
        if new_operating_mode and operating_mode != new_operating_mode:
            operating_mode = new_operating_mode
            sounds_effects.play_change_mode()

        # Notify currently active mode
        if handle_check_mode(control_inputs["check_mode"]):
            play_check_mode_sound(operating_mode, sounds_effects)

        # Sending Commands to arm
        if operating_mode == OperatingMode.ROBOTIC_ARM:
            arm_.handle_input(*control_inputs["arm"])

        time.sleep(0.01)

if __name__ == "__main__":
    main()
