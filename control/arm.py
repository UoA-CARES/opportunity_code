from .util import set_position, get_servo_position
from .servo_factory import servo_factory
import numpy as np
import time
# from cares_lib.dyanmixel.Servo improt Servo



class Arm:
    # define arm parameteres
    joint_limits = {
        "joint_0": [140, 175],
        "joint_1": [260, 325],
        "joint_2": [230, 310]
    }

    def __init__(self):

        self.servos = []

        # ids = [5, 6, 7, 8]
        self.ids = [5, 7, 8]
        # models =["MX-106", "MX-64", "MX-64", "XL430-W250-T"]
        # models =["MX-28", "MX-106", "MX-64", "XL430-W250-T"]
        self.models =["MX-28Protocol2", "MX-64Protocol2", "XL430-W250-T"]
        #Going toward the end of the arm, servos have ids 5-8
        for i in range(3):
            self.servos.append(
                servo_factory.create_servo(
                    model=self.models[i],
                    port="/dev/ttyUSB0",
                    # protocol=(1 if self.models[i][:2] in ["MX", "AX"] else 2),
                    protocol=(1 if self.models[i][:2] in ["AX"] else 2),
                    baudrate=1000000,
                    max=4095, #need to figure out range of motion, for now 45 degrees
                    min=0,
                    id = self.ids[i],
                )
            )


    def move_joint_simple(self, joint_id: int, step: int=5, direc: int=1, time: int=4000):
        is_limit_reached = 0
        # Set time profile
        self.set_profile_time(joints=[joint_id], time=time)

        # Read current servo position
        current_pos = get_servo_position(self.servos[joint_id])
        
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
        new_pos = int(new_pos * 4096 / 360)

        # Move servo to new_pos
        set_position([self.servos[joint_id]], [new_pos])
        return is_limit_reached
    
    def set_profile_time(self, joints: list[int], time):
        VEL_PROFILE_ADDR = 112

        for joint in joints:
            port_handler = self.servos[joint].port_handler
            packet_handler = self.servos[joint].packet_handler
            packet_handler.write4ByteTxRx(port_handler, self.ids[joint], VEL_PROFILE_ADDR, time)
    
    
    def handle_input(self, left_d_pad, right_d_pad, up_d_pad, down_d_pad, right_trigger, left_trigger):

        if left_d_pad == 1: # move vertical axis joint (arm base joint)
            self.move_joint_simple(joint_id=0, step=5, direc=-1, time=2000)

        elif right_d_pad == 1:# move vertical axis joint (arm base joint)
            self.move_joint_simple(joint_id=0, step=5, direc=1, time=2000)

        elif up_d_pad == 1: # move arm joint (arm joint)
            self.move_joint_simple(joint_id=1, step=5, direc=1, time=2000)

        if down_d_pad == 1: # move arm joint (arm joint)
            self.move_joint_simple(joint_id=1, step=5, direc=-1, time=2000)

        elif right_trigger > 0.1: # move camera joint
            self.move_joint_simple(joint_id=2, step=5, direc=1, time=2000)
        
        elif left_trigger > 0.1:
            self.move_joint_simple(joint_id=2, step=5, direc=-1, time=2000)

        else:
            pass

    def random_movement(self, step=5, time=3000):
        direc_0 = 1
        direc_1 = 1
        direc_2 = 1

        while True:
            limit_0 = self.move_joint_simple(joint_id=0, step=step, direc=direc_0, time=time)
            limit_1 = self.move_joint_simple(joint_id=1, step=step, direc=direc_1, time=time)
            limit_2 = self.move_joint_simple(joint_id=2, step=step, direc=direc_2, time=time)

            # Toggle direction
            if limit_0 is not 0:
                direc_0 *= -1
            if limit_1 is not 0:
                direc_1 *= -1
            if limit_2 is not 0:
                direc_2 *= -1

            time.sleep(time//1000)


    """
    def move_arm_joints(self, joint_id: int=0, joint_angle: int=0, time: int=2000, camera_horiz=False):
        
        self.set_profile_time(joints=[0, 1, 2], time=time)

        if joint_id == 0: 
            gear_ratio = 32 / 24
            joint_angle = (-joint_angle + 180) # 0 degrees when the servos are at 180 deg
            joint_angle = int((joint_angle) * gear_ratio * 4095 / 360) # add the effect of the gear ratio
            set_position(self.servos[0], [joint_angle])
        
        # if self.servos.model[joint_id] == 'MX-64': 
        elif joint_id == 1: 
            
            joint_angle_offset = (-joint_angle + 120) # 0 degrees when the servos are at 180 deg

            ARM_MIN = 120 - (-20)             
            ARM_MAX = 120 - (-45) # 165 # 120 - 165 = - 45 deg

            if joint_angle_offset < ARM_MIN: 
                joint_angle_offset = ARM_MIN
            elif joint_angle_offset > ARM_MAX: 
                joint_angle_offset = ARM_MAX
            else: 
                pass
            
            self.set_profile_time([joint_id], time)
            joint_angle_offset  = int((joint_angle_offset) * 4095 / 360) # add the effect of the gear ratio
            set_position([self.servos[1]], [joint_angle_offset])
            
            # keep the camera flat
            if camera_horiz == True:
                joint_angle_camera = -(joint_angle) + 180
                joint_angle_camera = int((joint_angle_camera) * 4095 / 360) # no offset
                set_position([self.servos[2]], [joint_angle_camera])
        
        elif joint_id == 2: 
            servo_1_pos = get_servo_position(self.servos[1])
            joint_angle_camera = -(joint_angle) + 180
            joint_angle_camera = int((joint_angle_camera) * 4095 / 360) # no offset
            set_position([self.servos[2]], [joint_angle_camera])

        else: 
            return
    """

    '''
    # simplified inverse kinematics for 3 DOF arm (rough approximation of the real arm)
    def simplified_inverse_kinematics(self, position: list[int]) -> list[int]:

        # define arm parameteres
        
        # L2, L3 = 1, 1 # TODO: update this
        x, y, z = position

        A = np.sqrt(x**2 + y**2)
        B = np.sqrt(A**2 + z**2)
        alpha = np.arctan2(z, A)     
        beta = self._cosines_law(self.L2, B, self.L3)
        gamma = self._cosines_law(self.L2, self.L3, B)
        
        # calculate theta1, theta2, theta3
        theta1 = np.arctan2(y, x)
        theta2 = alpha + beta
        theta3 = -(np.pi - gamma)
        
        # +ve using right hand rule
        # theta1: z-axis (pointing up), 0 degrees is along x-axis (pointing forward)
        # theta2: y-axis (pointing left), 0 degrees is along x-axis (pointing forward)
        # theta3: y-axis (pointing left), 0 degrees is along x-axis (pointing forward)
        return [theta1, theta2, theta3] 
    '''

    '''
    def move_arm(self, position: list[int]):
        
        gear_ratio = 32 / 24
        position = np.array(position)
        
        position[0] = position[0] + self.L2 + self.L3 - 100 # make the position relative to the most extended state -10 cm
        theta = self.simplified_inverse_kinematics(position) 
        theta = np.array(theta) * 180 / np.pi

        theta = (-theta + 180) # 0 degrees when the servos are at 180 deg
        theta[0] = int((theta[0]*gear_ratio) * 4095 / 360) # add the effect of the gear ratio
        theta[1] = int((theta[1] - 30) * 4095 / 360) # add 30 degrees offset 
        theta[2] = int((theta[2]) * 4095 / 360) # no offset
        
        # move servo
        set_position(self.servos, [int(theta[0]), int(theta[1]), int(theta[2])])

        '''
    
    '''
    @staticmethod
    def _cosines_law(l1, l2, opposite_l):
        return np.arccos((l1**2 + l2**2 - opposite_l**2)/(2*l1*l2))
    '''




# arm = Arm()
# arm.set_profile_time(joint=1, time=4000)
# arm.move_arm_joints(joint_id=1, joint_angle=-25, time=4000)
# arm.move_joint_simple(joint_id=1, step=5, direc=1, time=3000)
# arm.move_arm_joints(joint_id=1, joint_angle=0, time=2000)

# arm.move_arm_joints(joint_id=2, joint_angle=0, time=2000)










