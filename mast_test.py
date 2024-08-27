import time
from control import (
    handle_operating_mode,
    OperatingMode,
    Mast,
    XboxController,
    SoundEffects,
    handle_check_mode,
    play_check_mode_sound,
)


def main():

    max_angular_velocity = 200

    mast = Mast(max_angular_velocity)

    joy = XboxController()
    sounds_effects = SoundEffects()

    while True:

        control_inputs = joy.read()

        operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        new_operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        if new_operating_mode and operating_mode != new_operating_mode:
            operating_mode = new_operating_mode
            sounds_effects.play_change_mode()

        if handle_check_mode(control_inputs["check_mode"]):
            play_check_mode_sound(operating_mode, sounds_effects)

        # Sending Commands to Wheels
        if operating_mode == OperatingMode.DRIVE:
            mast.handle_input(*control_inputs["mast"])
        else:
            mast.stop_rotating()
            mast.stop_tilting()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
