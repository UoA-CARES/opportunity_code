import time
from control import XboxController, OperatingMode, handle_operating_mode, Wheels, SoundEffects, handle_check_mode, play_check_mode_sound
import vlc
import threading
from threading import Event


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

    end_event = Event()
    reset_event = Event()

    arm_stationary_mode_thread = threading.Thread(
        target=robotic_arm_stationary_mode, args=(end_event, reset_event)
    )

    camera_tracking_stationary_mode_thread = threading.Thread(
        target=camera_tracking_stationary_mode, args=(end_event, reset_event)
    )


    while True:

        control_inputs = joy.read()

        new_operating_mode = handle_operating_mode(control_inputs["operating_mode"])

        if new_operating_mode and operating_mode != new_operating_mode:
            operating_mode = new_operating_mode
            sounds_effects.play_change_mode()
        
        if handle_check_mode(control_inputs["check_mode"]):
            play_check_mode_sound(operating_mode, sounds_effects)

        # Kill stationary mode threads if not stationary mode
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

            if end_event.is_set():
                end_event.clear()
                reset_event.set()

            if not arm_stationary_mode_thread.is_alive():
                arm_stationary_mode_thread.start()

            if not camera_tracking_stationary_mode_thread.is_alive():
                camera_tracking_stationary_mode_thread.start()

        elif operating_mode == OperatingMode.EMERGENCY_STOP:
            # Send stop commands to all components
            pass
            # wheels.stop()

        time.sleep(0.01)

# Pass in arm object once integrated
def robotic_arm_stationary_mode(end_event: Event, reset_event: Event):

    i = 0
    while True:

        if end_event.is_set():
            reset_event.wait()

        print(f"Robotic Arm Stationary Mode {i}")
        time.sleep(1)

# Pass in camera and mast object once integrated
def camera_tracking_stationary_mode(end_event: Event, reset_event: Event):

    i = 0
    while True:
        if end_event.is_set():
            reset_event.wait()

        print(f"Camera Tracking Stationary Mode {i}")  
        i += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
