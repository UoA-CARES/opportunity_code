import time
from control import (
    handle_operating_mode,
    OperatingMode,
    Wheels,
    XboxController,
    SoundEffects,
    handle_check_mode,
    play_check_mode_sound,
)


def main():

    max_angular_velocity = 200
    max_linear_velocity = 200

    wheels = Wheels(
        max_linear_velocity=max_linear_velocity,
        max_angular_velocity=max_angular_velocity,
    )

    joy = XboxController()
    sounds_effects = SoundEffects()

    operating_mode = OperatingMode.EMERGENCY_STOP

    while True:

        control_inputs = joy.read()

        new_operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        # Change Operating Mode
        if new_operating_mode and operating_mode != new_operating_mode:
            operating_mode = new_operating_mode
            sounds_effects.play_change_mode()

        # Notify currently active mode
        if handle_check_mode(control_inputs["check_mode"]):
            play_check_mode_sound(operating_mode, sounds_effects)

        # Sending Commands to Wheels
        if operating_mode == OperatingMode.DRIVE:
            wheels.handle_input(*control_inputs["wheels"])
        else:
            wheels.stop()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
