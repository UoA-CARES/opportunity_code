from util import set_velocity
from servo_factory import servo_factory

class Mast:
    def __init__(self):

        self.servos = []

        #Servos located at the base of the mast and the head
        for _ in range(2):
            self.servos.append(
                servo_factory.create_servo(
                    model="XL430-W250-T",
                    port="/dev/ttyUSB0",
                    protocol=2,
                    baudrate=1000000,
                    max=4095,
                    min=0,
                )
            )

    def rotate_clockwise(self, speed):
        set_velocity([self.servos[0]], [speed])

    def rotate_counterclockwise(self, speed):
        set_velocity([self.servos[0]], [-speed])

    def tilt_up(self, speed):
        set_velocity([self.servos[1]], [speed])

    def tilt_down(self, speed):
        set_velocity([self.servos[1]], [-speed])

