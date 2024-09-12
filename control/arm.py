from .util import set_position, get_servo_position, set_servo_torque
from .servo_factory import servo_factory
import numpy as np
import time



class Arm:
    # define arm parameteres
    joint_limits = {
        "joint_0": [150, 225],
        "joint_1": [260, 310],
        "joint_2": [230, 310]
    }

    def __init__(self):

        self.servos = []

        self.ids = [5, 7, 8]

        self.models =["MX-28Protocol2", "MX-64Protocol2", "XL430-W250-T"]
        
        self.current_pose = 0 

        self.poses = {
                0: [150, 280, 260],
                1: [225, 300, 300],
                2: [175, 260, 240],



            } # define motion here
        
        self.home_position = [2000, 3343, 3061]

        for i in range(3):
            self.servos.append(
                servo_factory.create_servo(
                    model=self.models[i],
                    port="/dev/ttyArm",
                    protocol=(1 if self.models[i][:2] in ["AX"] else 2),
                    baudrate=1000000,
                    max=4095, #need to figure out range of motion, for now 45 degrees
                    min=0,
                    id = self.ids[i],
                )
            )

    def move_random(self, active_joints: list=[0, 1, 2], t: int=4000):

        # Set time profile
        self.set_profile_time(joints=active_joints, t=t)

        set_servo_torque(self.servos[0], enable=True) # Enable torque for joint 0

        new_poses= self.poses[self.current_pose] # Get servo angles
        for joint in active_joints:
            pos = new_poses[joint]
            # Check if withing limts
            if pos > self.joint_limits[f"joint_{joint}"][1]:
                pos = self.joint_limits[f"joint_{joint}"][1]
            elif pos < self.joint_limits[f"joint_{joint}"][0]:
                pos = self.joint_limits[f"joint_{joint}"][0]
            
            new_pos = int(pos * 4096 / 360)
            set_position([self.servos[joint]], [new_pos])

        self.current_pose += 1 # Update the next pose
        self.current_pose %= len(self.poses) # Making sure to not exceed the available number of poses
        time.sleep(t//1000)

        set_servo_torque(self.servos[0], enable=False) # Disable torque for joint 0
        

    def move_joint_simple(self, joint_id: int, step: int=5, direc: int=1, t: int=4000):
        is_limit_reached = 0
        # Set time profile
        self.set_profile_time(joints=[joint_id], t=t)

        if joint_id == 0: 
            set_servo_torque(self.servos[joint_id], enable=True)

        # Read current servo position
        current_pos = int(get_servo_position(self.servos[joint_id]) * 360 / 4096)
        print(f'current {current_pos}')
        # Step the position bu POS_STEP
        new_pos = current_pos + step if direc > 0 else current_pos - step

        # Check if withing limts
        if new_pos > self.joint_limits[f"joint_{joint_id}"][1]:
            new_pos = self.joint_limits[f"joint_{joint_id}"][1]
            is_limit_reached = 1
        elif new_pos < self.joint_limits[f"joint_{joint_id}"][0]:
            new_pos = self.joint_limits[f"joint_{joint_id}"][0]
            is_limit_reached = -1
        # Convert degrees to positions
        print(f"{joint_id}: move to {new_pos}")
        new_pos = int(new_pos * 4096 / 360)
        

        # Move servo to new_pos
        set_position([self.servos[joint_id]], [new_pos])
        time.sleep(t//1000 - 0.1)
        if joint_id == 0: 
            set_servo_torque(self.servos[joint_id], enable=False)
        return is_limit_reached
    
    def set_profile_time(self, joints: list[int], t):
        VEL_PROFILE_ADDR = 112

        for joint in joints:
            port_handler = self.servos[joint].port_handler
            packet_handler = self.servos[joint].packet_handler
            packet_handler.write4ByteTxRx(port_handler, self.ids[joint], VEL_PROFILE_ADDR, t)
    
    
    def handle_input(self, d_pad_x, d_pad_y, right_trigger, left_trigger):

        if d_pad_x == -1: # move vertical axis joint (arm base joint)
            self.move_joint_simple(joint_id=0, step=25, direc=-1, t=2000)

        elif d_pad_x == 1:# move vertical axis joint (arm base joint)
            self.move_joint_simple(joint_id=0, step=25, direc=1, t=2000)

        elif d_pad_y == 1: # move arm joint (arm joint)
            self.move_joint_simple(joint_id=1, step=5, direc=1, t=1500)

        if d_pad_y == -1: # move arm joint (arm joint)
            self.move_joint_simple(joint_id=1, step=5, direc=-1, t=1500)

        elif right_trigger > 0.1: # move camera joint
            self.move_joint_simple(joint_id=2, step=15, direc=1, t=1000)
        
        elif left_trigger > 0.1:
            self.move_joint_simple(joint_id=2, step=15, direc=-1, t=1000)

    def move_to_home(self):
        set_position(self.servos, self.home_position)










