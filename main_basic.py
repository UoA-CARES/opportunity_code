import time
from control import (
    Mast,
    FaceTracker,
    SoundEffects,
)


def main():
    mast_ang_vel = 20

    # Instantiate the Components
    mast = Mast(max_servo_speed=mast_ang_vel)

    _ = SoundEffects()
    face_tracker = FaceTracker(replacement_mode="all")

    while face_tracker.is_facetracker():

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
