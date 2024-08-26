# to test arm control code
# from servo_factory import servo_factory
# from control.util import set_position

import numpy as np
from numpy import array, sin, cos, pi
import matplotlib.pyplot as plt

class Arm:

    

    def __init__(self):
        pass
        # self.servos = []
        #
        # ids = [5, 6, 7, 8]
        # models =["MX-106", "MX-64", "MX-64", "XL430-W250-T"]
        #
        # #Going toward the end of the arm, servos have ids 5-8
        # for i in range(4):
        #     self.servos.append(
        #         servo_factory.create_servo(
        #             model=models[i],
        #             port="/dev/ttyUSB0",
        #             protocol=(1 if models[i][:2] in ["MX", "AX"] else 2),
        #             baudrate=1000000,
        #             max=4095//8, #need to figure out range of motion, for now 45 degrees
        #             min=0,
        #             id = ids[i],
        #         )
        #     )
        #

    # def rotate_joint_clockwise(self, id, position):
    #     set_position([self.servos[id-5]], [position])
    #
    # def rotate_joint_counterclockwise(self, id, position):
    #     set_position([self.servos[id-5]], [position])
    #

    def simplified_inverse_kinematics(self, position: list[int]) -> list[int]:

        # define arm parameteres
        # L2, L3 = 380, 368 # TODO: update this
        L2, L3 = 1, 1 # TODO: update this
        x, y, z = position

        # calculate theta1
        theta1 = np.arctan2(y, x)

        A = np.sqrt(x**2 + y**2)
        B = np.sqrt(A**2 + z**2)
        alpha = np.arctan2(z, A)     
        beta = self._cosines_law(L2, B, L3)
        gamma = self._cosines_law(L2, L3, B)
        theta2 = alpha + beta
        theta3 = -(np.pi - gamma)

        return [theta1, theta2, theta3]

    @staticmethod
    def _cosines_law(l1, l2, opposite_l):
        return np.arccos((l1**2 + l2**2 - opposite_l**2)/(2*l1*l2))

def plot_finger(T_matrices):

    # Extract positions of each frame in homogeneous coordinates
    positions = []
    for T in T_matrices:
        positions.append((T @ np.array([0, 0, 0, 1]))[:3])
    positions = np.array(positions)

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')

    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], marker='o')

    X, Y, Z = positions[:, 0], positions[:, 1], positions[:, 2]
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0

    # Set the limits of the plot
    mid_x = (X.max()+X.min()) * 0.5
    mid_y = (Y.max()+Y.min()) * 0.5
    mid_z = (Z.max()+Z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Set labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Finger Joint Positions')
    plt.show()

def rotation_matrix(angles, is_rad=False) -> np.ndarray:
    theta_x, theta_y, theta_z = angles[0], angles[1], angles[2]
    if not is_rad:
        theta_x, theta_y, theta_z = np.deg2rad(theta_x), np.deg2rad(theta_y), np.deg2rad(theta_z)

    # Rotation matrix from the base frame to the platform frame
    R_x = np.array([
        [1, 0, 0],
        [0, cos(theta_x), -sin(theta_x)],
        [0, sin(theta_x), cos(theta_x)]])    
    
    R_y = np.array([
        [cos(theta_y), 0, sin(theta_y)],
        [0, 1, 0], 
        [-sin(theta_y), 0, cos(theta_y)]])
    
    R_z = np.array([
        [cos(theta_z), -sin(theta_z), 0], 
        [sin(theta_z), cos(theta_z), 0],
        [0, 0, 1]])
    
    return R_z.dot(R_y.dot(R_x))

def trans_matrix(translation) -> np.ndarray:
    T = np.eye(4)
    T[:3, 3] = translation
    return T


def homogeneous_transform(R, P, is_rad=True) -> np.ndarray: # Homogeneous transformation matrix
    T = np.eye(4)
    T[:3, :3] = rotation_matrix(R, is_rad)
    T[:3, 3] = P
    return T

arm = Arm()


goal = [1, -1, -0.5]

theta1, theta2, theta3 = Arm().simplified_inverse_kinematics(goal)

T_1_0 = homogeneous_transform([0, 0, 0], np.array([0, 0, 0]))
T_2_1 = homogeneous_transform([0, 0, theta1], np.array([0, 0, 0]))
T_3_2 = homogeneous_transform([0, -theta2, 0], np.array([0, 0, 0]))
T_4_3 = homogeneous_transform([0, 0, 0], np.array([1, 0, 0]))
T_5_4 = homogeneous_transform([0, -theta3, 0], np.array([0, 0, 0]))
T_6_5 = homogeneous_transform([0, 0, 0], np.array([1, 0, 0]))


# Forward kinematics: transformation matrix from frame 9 to frame 0
T_6_0 = T_1_0 @ T_2_1 @ T_3_2 @ T_4_3 @ T_5_4 @ T_6_5


# Define the transformations for frames 0, 2, 4, 6, 8, and 9 relative to frame 0
T_2_0 = T_1_0 @ T_2_1
T_4_0 = T_2_0 @ T_3_2 @ T_4_3
T_6_0 = T_4_0 @ T_5_4 @ T_6_5



# List of transformation matrices to be plotted
T_matrices = [T_1_0, T_4_0, T_6_0, homogeneous_transform([0, 0, 0], np.array(goal))]
# print(T_matrices)
plot_finger(T_matrices)



