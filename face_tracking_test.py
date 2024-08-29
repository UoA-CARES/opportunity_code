import time
from control import (
    XboxController,
    OperatingMode,
    handle_operating_mode,
    Wheels,
    Mast,
    FaceTracker,
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
    face_tracker = FaceTracker(replacement_mode="one")

    while not face_tracker.is_facetracker():
        print("Waiting for face tracker to start")
        time.sleep(1)
    
    operating_mode = OperatingMode.STATIONARY

    # Set up background threads for stationary mode
    end_event = Event()
    reset_event = Event()

    background_thread = threading.Thread(
        target=background_control, args=(mast, face_tracker, end_event, reset_event)
    )

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
            mast.handle_input(*control_inputs["mast"])
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

            if not background_thread.is_alive():
                background_thread.start()


        elif operating_mode == OperatingMode.EMERGENCY_STOP:
            # Send stop commands to all components
            pass
            # wheels.stop()

        time.sleep(0.01)


def background_control(mast: Mast, face_tracker: FaceTracker, end_event: Event, reset_event: Event):

    i = 0
    while face_tracker.is_facetracker():

        if end_event.is_set():
            mast.stop_rotating()
            mast.stop_tilting()
            reset_event.wait()

        x_direction = face_tracker.get_move_horizontal()
        y_direction = face_tracker.get_move_vertical()

        if x_direction == 1:
            mast.rotate_counterclockwise(10)
            print("Rotating counterclockwise")
        elif x_direction == -1:
            mast.rotate_clockwise(10)
            print("Rotating clockwise")
        else:
            mast.stop_rotating()
            print("Stopping rotation")

        if y_direction == 1:
            mast.tilt_down(10)
            print("Tilting down")
        elif y_direction == -1:
            mast.tilt_up(10)
            print("Tilting up")
        else:
            mast.stop_tilting()
            print("Stopping tilt")
        
        print("------------")
         
        time.sleep(0.1)
        i += 1



if __name__ == "__main__":
    main()
