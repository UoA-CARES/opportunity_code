import time
from control import XboxController, OperatingMode, handle_operating_mode, Wheels, SoundEffects
import vlc

def main():

    max_angular_velocity = 200
    max_linear_velocity = 500

    # # Instantiate the Components
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
            print('Changed')
        


        time.sleep(0.01)


if __name__ == "__main__":
    main()
