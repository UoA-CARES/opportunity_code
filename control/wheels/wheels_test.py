import time
from xbox_controller import XboxController
from wheels import Wheels

def main():

    standard_servo_velocity = 200

    wheels = Wheels()
    
    joy = XboxController()

    emergency_stop = True

    while True:

        control_inputs = joy.read()

        left_joy_x, left_joy_y, right_trigger, left_trigger, A_button = control_inputs
        left_joy_x = round(left_joy_x, 1)

        # A button is used for emergency stopping. Can be toggled
        if A_button > 0:
            emergency_stop = not emergency_stop
        
        # Sending Commands to Wheels
        if emergency_stop == False:
            if right_trigger > 0.1:
                val = round(500 * right_trigger/1)
                wheels.move_forward(val)
            if left_trigger > 0.1:
                val = round(500 * left_trigger/1)
                wheels.move_backward(val)
            if left_joy_x > 0.5:
                wheels.turn_counter_clockwise(standard_servo_velocity)
            if left_joy_x < -0.5: 
                wheels.turn_clockwise(standard_servo_velocity)
        else:
            wheels.stop()

        time.sleep(0.01)


if __name__ == "__main__":
    main()