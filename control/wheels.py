from util import set_velocity
from servo_factory import servo_factory

class Wheels:
    def __init__(self):

        self.servos = []

        # Left and right wheels
        for _ in range(2):
            self.servos.append(
                servo_factory.create_servo(
                    model="MX-106",
                    port="/dev/ttyUSB0",
                    protocol=1,
                    baudrate=1000000,
                    max=4095,
                    min=0,
                )
            )

    def move_forward(self, speed):
        set_velocity(self.servos, [speed, speed])

    def move_backward(self, speed):
        set_velocity(self.servos, [-speed, -speed])

    def turn_clockwise(self, speed):
        set_velocity(self.servos, [-speed, speed])

    def turn_counter_clockwise(self, speed):
        set_velocity(self.servos, [speed, -speed])

    def stop(self):
        set_velocity(self.servos, [0, 0])
