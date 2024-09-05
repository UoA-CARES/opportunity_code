from .util import set_velocity
from .servo_factory import servo_factory



class Wheels:
    def __init__(self, max_linear_velocity=200, max_angular_velocity=200):
        
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

    def turn(self, left_speed, right_speed):
        set_velocity(self.servos, [-left_speed, right_speed])

    def stop(self):
        set_velocity(self.servos, [0, 0])

    def handle_input(self, left_joy_x, right_trigger, left_trigger):
        """
        Joy values are between 0 and 1
        Trigger values are between 0 and 1

        left_joy_x: -1 is left, 1 is right
        right_trigger: 0 is not pressed, 1 is fully pressed
        left_trigger: 0 is not pressed, 1 is fully pressed
        """

        # Turn left
        if left_joy_x < -0.1 and right_trigger > 0.1:
            self.turn(
                round(self.max_linear_velocity * right_trigger),
                round(self.max_linear_velocity * right_trigger * (1 + left_joy_x)),
            )
        
        # Turn right
        elif left_joy_x > 0.1 and right_trigger > 0.1:
            self.turn(
                round(self.max_linear_velocity * right_trigger * (1 - left_joy_x)),
                round(self.max_linear_velocity * right_trigger),
            )
        
        # Backward left
        elif left_joy_x < -0.1 and left_trigger > 0.1:
            self.turn(
                round(-self.max_linear_velocity * left_trigger),
                round(-self.max_linear_velocity * left_trigger * (1 + left_joy_x)),
            )

        # Backward right
        elif left_joy_x > 0.1 and left_trigger > 0.1:
            self.turn(
                round(-self.max_linear_velocity * left_trigger * (1 - left_joy_x)),
                round(-self.max_linear_velocity * left_trigger),
            )

        elif right_trigger > 0.1:
            val = round(self.max_linear_velocity * right_trigger)
            self.move_forward(val)
        elif left_trigger > 0.1:
            val = round(self.max_linear_velocity * left_trigger)
            self.move_backward(val)
        elif left_joy_x > 0.5:
            self.turn_clockwise(self.max_angular_velocity)
        elif left_joy_x < -0.5:
            self.turn_counter_clockwise(self.max_angular_velocity)
        else:
            self.stop()
