from .util import set_velocity, get_servo_position
from .servo_factory import servo_factory


class Mast:
    def __init__(self, max_servo_speed=20):

        self.servo_speed = max_servo_speed
        self.servos = []

        # Servos located at the base of the mast and the head, with ids 3 and 4
        for i in range(3, 5):
            self.servos.append(
                servo_factory.create_servo(
                    model="XL430-W250-T" if i == 3 else "MX-28",
                    port="/dev/ttyUSB1",
                    protocol=2 if i == 3 else 1,
                    baudrate=1000000,
                    # head servo needs to be limited to a range of motion of 90 degrees
                    max=4095 if i == 3 else 1024,
                    min=0,
                    id=i,
                )
            )

        self.MAX_SERVO_POSITIONS = [4095, 1800]
        self.MIN_SERVO_POSITIONS = [0, 1300]

    def is_tilt_too_cw(self):
        return get_servo_position(self.servos[1]) <= self.MIN_SERVO_POSITIONS[1]
    
    def is_tilt_too_ccw(self):
        return get_servo_position(self.servos[1]) >= self.MAX_SERVO_POSITIONS[1]
    
    def is_rotation_too_cw(self):
        return get_servo_position(self.servos[0]) <= self.MIN_SERVO_POSITIONS[0]
    
    def is_rotation_too_ccw(self):
        return get_servo_position(self.servos[0]) >= self.MAX_SERVO_POSITIONS[0]

    def rotate_clockwise(self, speed):

        if not self.is_rotation_too_cw():
            return

        set_velocity([self.servos[0]], [speed])

    def rotate_counterclockwise(self, speed):

        if not self.is_rotation_too_ccw():
            return

        set_velocity([self.servos[0]], [-speed])

    def stop_rotating(self):
        set_velocity([self.servos[0]], [0])

    def tilt_up(self, speed):

        if not self.is_tilt_too_ccw():
            return

        set_velocity([self.servos[1]], [speed])

    def tilt_down(self, speed):

        if not self.is_tilt_too_cw():
            return

        set_velocity([self.servos[1]], [-speed])

    def stop_tilting(self):
        set_velocity([self.servos[1]], [0])

    def handle_input(self, right_bumper, left_bumper, right_joy_y):

        right_joy_y = round(right_joy_y, 1)
        if right_bumper == 1:
            self.rotate_clockwise(self.servo_speed)
        elif left_bumper == 1:
            self.rotate_counterclockwise(self.servo_speed)
        else:
            self.stop_rotating()

        if right_joy_y > 0.5:
            self.tilt_up(self.servo_speed)
        elif right_joy_y < -0.5:
            self.tilt_down(self.servo_speed)
        else:
            self.stop_tilting()
