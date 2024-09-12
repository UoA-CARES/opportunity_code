import time
from control import (
    XboxController,
    OperatingMode,
    handle_operating_mode,
    Mast,
    Arm,
    FaceTracker,
    SoundEffects,
    handle_check_mode,
    play_check_mode_sound,
)
import threading
from threading import Event


def main():

    wheels_lin_vel = 200
    wheels_ang_vel = 200

    mast_ang_vel = 20

    # Instantiate the Components
    mast = Mast(max_angular_velocity=mast_ang_vel)
    arm = Arm()

    joy = XboxController()
    sounds_effects = SoundEffects()
    face_tracker = FaceTracker(replacement_mode="one")

    operating_mode = OperatingMode.EMERGENCY_STOP

    # Set up background threads for stationary mode
    end_event = Event()
    reset_event = Event()

    arm_stationary_mode_thread = threading.Thread(
        target=robotic_arm_stationary_mode, args=(arm, end_event, reset_event)
    )

    camera_tracking_stationary_mode_thread = threading.Thread(
        target=camera_tracking_stationary_mode, args=(mast, face_tracker, end_event, reset_event)
    )

    arm_stationary_mode_thread.start()
    camera_tracking_stationary_mode_thread.start()

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

        # Pause the stationary background threads when not in stationary mode
        if operating_mode != OperatingMode.STATIONARY:
            end_event.set()
            reset_event.clear()

        # Drive the wheels and mast
        if operating_mode == OperatingMode.DRIVE:
            pass

        # Control the robotic arm
        elif operating_mode == OperatingMode.ROBOTIC_ARM:
            arm.handle_input(*control_inputs["arm"])

        # Robotic arm moves to random set positions
        # Camera and Mast tracks the faces of participants
        elif operating_mode == OperatingMode.STATIONARY:

            # Reset the flags for the stationary mode threads
            if end_event.is_set():
                end_event.clear()
                reset_event.set()
        
        # Stop all components
        elif operating_mode == OperatingMode.EMERGENCY_STOP:
            mast.stop_rotating()
            mast.stop_tilting()
            arm.move_to_home()

        time.sleep(0.01)


def robotic_arm_stationary_mode(arm: Arm, end_event: Event, reset_event: Event):

    while True:

        if end_event.is_set():
            arm.move_to_home()
            reset_event.wait()

        arm.move_random(t=4000)
        time.sleep(3)


def camera_tracking_stationary_mode(mast: Mast, face_tracker: FaceTracker, end_event: Event, reset_event: Event):

    while face_tracker.is_facetracker():

        if end_event.is_set():
            mast.stop_rotating()
            mast.stop_tilting()
            reset_event.wait()

        x_direction = face_tracker.get_move_horizontal()
        y_direction = face_tracker.get_move_vertical()

        if x_direction == 1:
            mast.rotate_clockwise(20)
        elif x_direction == -1:
            mast.rotate_counterclockwise(20)
        else:
            mast.stop_rotating()

        if y_direction == 1:
            mast.tilt_down(10)
        elif y_direction == -1:
            mast.tilt_up(10)
        else:
            mast.stop_tilting()
         
        time.sleep(0.1)


if __name__ == "__main__":
    main()
