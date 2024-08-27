import time
from control import XboxController, OperatingMode, handle_operating_mode, Wheels, SoundEffects, handle_check_mode, play_check_mode_sound
import vlc

def main():

    max_angular_velocity = 200
    max_linear_velocity = 500

    # Instantiate the Components
    # wheels = Wheels(
    #     max_linear_velocity=max_linear_velocity,
    #     max_angular_velocity=max_angular_velocity,
    # )

    joy = XboxController()
    sounds_effects = SoundEffects()
    operating_mode = OperatingMode.STATIONARY

    while True:

        control_inputs = joy.read()

        new_operating_mode = handle_operating_mode(control_inputs["operating_mode"])
        
        if new_operating_mode and operating_mode != new_operating_mode:
            operating_mode = new_operating_mode
            sounds_effects.play_change_mode()
        
        if handle_check_mode(control_inputs["check_mode"]):
            play_check_mode_sound(operating_mode, sounds_effects)

        if operating_mode == OperatingMode.DRIVE:
            # Use Controller to drive the rover and control the mast
            print("DRIVE")
            # wheels.handle_inputs(control_inputs["wheels"])
        elif operating_mode == OperatingMode.ROBOTIC_ARM:
            # Use Controller to control the robotic arm
            print("ROBOTIC_ARM")
        elif operating_mode == OperatingMode.STATIONARY:
            # Stationary mode
            # Random robotic arm movement
            # Camera track face, alien thing
            print("STATIONARY")
        elif operating_mode == OperatingMode.EMERGENCY_STOP:
            # Send stop commands to all components
            print("EMERGENCY_STOP")
            # wheels.stop()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
