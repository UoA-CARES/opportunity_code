
import time
import threading
from threading import Event
from control import (
    handle_operating_mode,
    OperatingMode,
    Arm ,
    XboxController,
    SoundEffects,
    handle_check_mode,
    play_check_mode_sound,
)


def main():


    arm = Arm()

    joy = XboxController()
    sounds_effects = SoundEffects()

    operating_mode = OperatingMode.EMERGENCY_STOP
    
    end_event = Event()
    reset_event = Event()

    end_event.set()
    reset_event.clear()

    background_thread = threading.Thread(
        target=background_control, args=(arm, end_event, reset_event)
    )


    background_thread.start()
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

        # Pause the stationary background threads if the operating mode is not stationary
        if operating_mode != OperatingMode.STATIONARY:
            end_event.set()
            reset_event.clear()

        # Sending Commands to arm
        if operating_mode == OperatingMode.ROBOTIC_ARM:
            arm.handle_input(*control_inputs["arm"])
        elif operating_mode == OperatingMode.STATIONARY:

            # Reset the flags for the stationary mode threads
            if end_event.is_set():
                end_event.clear()
                reset_event.set()
            
            

        time.sleep(0.01)

def background_control(arm: Arm, end_event: Event, reset_event: Event):

    while True:

        if end_event.is_set():
            arm.move_to_home()
            reset_event.wait()

        arm.move_random(t=4000)
        time.sleep(3)


if __name__ == "__main__":
    main()
