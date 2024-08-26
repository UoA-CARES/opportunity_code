from util import set_position
from servo_factory import servo_factory

import numpy as np

class Arm:
    
    def __init__(self):

        self.servos = []

        ids = [5, 6, 7, 8]
        models =["MX-106", "MX-64", "MX-64", "XL430-W250-T"]

        #Going toward the end of the arm, servos have ids 5-8
        for i in range(4):
            self.servos.append(
                servo_factory.create_servo(
                    model=models[i],
                    port="/dev/ttyUSB0",
                    protocol=(1 if models[i][:2] in ["MX", "AX"] else 2),
                    baudrate=1000000,
                    max=4095//8, #need to figure out range of motion, for now 45 degrees
                    min=0,
                    id = ids[i],
                )
            )

    # simplified inverse kinematics for 3 DOF arm (rough approximation of the real arm)
    def simplified_inverse_kinematics(self, position: list[int]) -> list[int]:

        # define arm parameteres
        L2, L3 = 380, 368 # TODO: update this
        # L2, L3 = 1, 1 # TODO: update this
        x, y, z = position

        A = np.sqrt(x**2 + y**2)
        B = np.sqrt(A**2 + z**2)
        alpha = np.arctan2(z, A)     
        beta = self._cosines_law(L2, B, L3)
        gamma = self._cosines_law(L2, L3, B)
        
        # calculate theta1, theta2, theta3
        theta1 = np.arctan2(y, x)
        theta2 = alpha + beta
        theta3 = -(np.pi - gamma)
        
        # +ve using right hand rule
        # theta1: z-axis (pointing up), 0 degrees is along x-axis (pointing forward)
        # theta2: y-axis (pointing left), 0 degrees is along x-axis (pointing forward)
        # theta3: y-axis (pointing left), 0 degrees is along x-axis (pointing forward)
        return [theta1, theta2, theta3]


    def rotate_joint_clockwise(self, id, position):
        set_position([self.servos[id-5]], [position])

    def rotate_joint_counterclockwise(self, id, position):
        set_position([self.servos[id-5]], [position])

    @staticmethod
    def _cosines_law(l1, l2, opposite_l):
        return np.arccos((l1**2 + l2**2 - opposite_l**2)/(2*l1*l2))
