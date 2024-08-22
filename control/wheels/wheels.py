from util import set_velocity
from servo_factory import servo_factory

class Wheels:
    def __init__(self):

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
                    id = i
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
    
    def handle_input(self, right_trigger, left_trigger, left_joy_x, velocity):
        if right_trigger > 0.1:
            val = round(500 * right_trigger/1)
            self.move_forward(val)
        if left_trigger > 0.1:
            val = round(500 * left_trigger/1)
            self.move_backward(val)
        if left_joy_x > 0.5:
            self.turn_counter_clockwise(velocity)
        if left_joy_x < -0.5: 
            self.turn_clockwise(velocity)
