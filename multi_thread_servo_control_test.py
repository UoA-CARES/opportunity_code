import time
from control import (
    XboxController,
    OperatingMode,
    handle_operating_mode,
    Mast,
    SoundEffects,
    handle_check_mode,
    play_check_mode_sound,
)
import threading
from threading import Event


def main():

    mast = Mast()

    joy = XboxController()
    sounds_effects = SoundEffects()

    operating_mode = OperatingMode.EMERGENCY_STOP

    # Set up background threads for stationary mode
    end_event = Event()
    reset_event = Event()

    # Pause background threads on start
    end_event.set()
    reset_event.clear()

    thread_one = threading.Thread(
        target=thread_one_control, args=(mast, end_event, reset_event)
    )

    thread_two = threading.Thread(
        target=thread_two_control, args=(mast, end_event, reset_event)
    )

    thread_one.daemon = True
    thread_two.daemon = True
    
    thread_one.start()
    thread_two.start()

    while True:

        control_inputs = joy.read()

        new_operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        # Alert the user if the operating mode has changed
        if new_operating_mode and operating_mode != new_operating_mode:
            operating_mode = new_operating_mode
            sounds_effects.play_change_mode()

        # If user wants to check mode, play the sound effect for the current mode
        if handle_check_mode(control_inputs["check_mode"]):
            play_check_mode_sound(operating_mode, sounds_effects)

        # Pause the stationary background threads if the operating mode is not stationary
        if operating_mode != OperatingMode.STATIONARY:
            end_event.set()
            reset_event.clear()

        if operating_mode == OperatingMode.DRIVE:
            # Use Controller to drive the rover and control the mast
            pass
            # wheels.handle_inputs(control_inputs["wheels"])
        elif operating_mode == OperatingMode.ROBOTIC_ARM:
            # Use Controller to control the robotic arm
            pass
        elif operating_mode == OperatingMode.STATIONARY:
            # Stationary mode
            # Random robotic arm movement
            # Camera track face, alien thing

            # Reset the flags for the stationary mode threads
            if end_event.is_set():
                end_event.clear()
                reset_event.set()

        elif operating_mode == OperatingMode.EMERGENCY_STOP:
            # Send stop commands to all components
            pass
            # wheels.stop()

        time.sleep(0.01)


def thread_one_control(mast: Mast, end_event: Event, reset_event: Event):

    i = 0
    while True:

        if end_event.is_set():
            reset_event.wait()

        time.sleep(1)
        print(f"Thread one speaking {i}")
        mast.rotate_counterclockwise(50)
        i += 1



def thread_two_control(mast: Mast, end_event: Event, reset_event: Event):

    i = 0
    while True:
        if end_event.is_set():
            reset_event.wait()

        mast.rotate_clockwise(50)
        print(f"Thread two speaking {i}")
        time.sleep(1)
        i += 1


if __name__ == "__main__":
    main()
