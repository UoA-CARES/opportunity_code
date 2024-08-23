from .util import set_velocity
from .servo_factory import servo_factory


class Wheels:
    def __init__(self, max_linear_velocity=500, max_angular_velocity=200):
        
        self.max_linear_velocity = max_linear_velocity
        self.max_angular_velocity = max_angular_velocity

        self.servos = []

        # Left and right wheels, with ids 1 and 2
        for i in range(1, 3):
            self.servos.append(
                servo_factory.create_servo(
                    model="MX-106",
                    port="/dev/ttyUSB0",
                    protocol=1,
                    baudrate=1000000,
                    max=4095,
                    min=0,
                    id=i,
                )
            )

    def move_forward(self, speed):
        set_velocity(self.servos, [-speed, speed])

    def move_backward(self, speed):
        set_velocity(self.servos, [speed, -speed])

    def turn_clockwise(self, speed):
        set_velocity(self.servos, [speed, speed])

    def turn_counter_clockwise(self, speed):
        set_velocity(self.servos, [-speed, -speed])

    def stop(self):
        set_velocity(self.servos, [0, 0])

    def handle_input(self, right_trigger, left_trigger, left_joy_x):
        if right_trigger > 0.1:
            val = round(self.max_linear_velocity * right_trigger)
            self.move_forward(val)
        elif left_trigger > 0.1:
            val = round(self.max_linear_velocity * left_trigger)
            self.move_backward(val)
        elif left_joy_x > 0.5:
            self.turn_counter_clockwise(self.max_angular_velocity)
        elif left_joy_x < -0.5:
            self.turn_clockwise(self.max_angular_velocity)
        else:
            self.stop()
