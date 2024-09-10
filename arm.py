# from control.util import set_position
# from control.servo_factory import servo_factory
# import numpy as np
# import time
# # from cares_lib.dyanmixel.Servo improt Servo
#
# class Arm:
#     # define arm parameteres
#     L2, L3 = 380, 368 # TODO: update this
#
#     def __init__(self):
#
#         self.servos = []
#
#         # ids = [5, 6, 7, 8]
#         self.ids = [5, 7, 8]
#         # models =["MX-106", "MX-64", "MX-64", "XL430-W250-T"]
#         # models =["MX-28", "MX-106", "MX-64", "XL430-W250-T"]
#         self.models =["MX-28Protocol2", "MX-64Protocol2", "XL430-W250-T"]
#         #Going toward the end of the arm, servos have ids 5-8
#         for i in range(3):
#             self.servos.append(
#                 servo_factory.create_servo(
#                     model=self.models[i],
#                     port="/dev/ttyUSB0",
#                     # protocol=(1 if self.models[i][:2] in ["MX", "AX"] else 2),
#                     protocol=(1 if self.models[i][:2] in ["AX"] else 2),
#                     baudrate=1000000,
#                     max=4095, #need to figure out range of motion, for now 45 degrees
#                     min=0,
#                     id = self.ids[i],
#                 )
#             )
#
#
#     # simplified inverse kinematics for 3 DOF arm (rough approximation of the real arm)
#     def simplified_inverse_kinematics(self, position: list[int]) -> list[int]:
#
#         # define arm parameteres
#
#         # L2, L3 = 1, 1 # TODO: update this
#         x, y, z = position
#
#         A = np.sqrt(x**2 + y**2)
#         B = np.sqrt(A**2 + z**2)
#         alpha = np.arctan2(z, A)     
#         beta = self._cosines_law(self.L2, B, self.L3)
#         gamma = self._cosines_law(self.L2, self.L3, B)
#
#         # calculate theta1, theta2, theta3
#         theta1 = np.arctan2(y, x)
#         theta2 = alpha + beta
#         theta3 = -(np.pi - gamma)
#
#         # +ve using right hand rule
#         # theta1: z-axis (pointing up), 0 degrees is along x-axis (pointing forward)
#         # theta2: y-axis (pointing left), 0 degrees is along x-axis (pointing forward)
#         # theta3: y-axis (pointing left), 0 degrees is along x-axis (pointing forward)
#         return [theta1, theta2, theta3]
#
#
#     def move_arm(self, position: list[int]):
#
#         gear_ratio = 32 / 24
#         position = np.array(position)
#
#         position[0] = position[0] + self.L2 + self.L3 - 100 # make the position relative to the most extended state -10 cm
#         theta = self.simplified_inverse_kinematics(position) 
#         theta = np.array(theta) * 180 / np.pi
#
#         theta = (-theta + 180) # 0 degrees when the servos are at 180 deg
#         theta[0] = int((theta[0]*gear_ratio) * 4095 / 360) # add the effect of the gear ratio
#         theta[1] = int((theta[1] - 30) * 4095 / 360) # add 30 degrees offset 
#         theta[2] = int((theta[2]) * 4095 / 360) # no offset
#
#         # move servo
#         set_position(self.servos, [int(theta[0]), int(theta[1]), int(theta[2])])
#
#
#     def move_arm_joints(self, joint_id: int=0, joint_angle: int=0, time: int=2000):
#
#
#
#         # 120 
#         self.set_profile_time(0, time)
#         self.set_profile_time(1, time)
#         self.set_profile_time(2, time)
#
#         if joint_id == 0: 
#             gear_ratio = 32 / 24
#             joint_angle = (-joint_angle + 180) # 0 degrees when the servos are at 180 deg
#             joint_angle = int((joint_angle) * 4095 / 360) # add the effect of the gear ratio
#             set_position(self.servos[0], [joint_angle])
#
#         # if self.servos.model[joint_id] == 'MX-64': 
#         if joint_id == 1: 
#
#             joint_angle_offset = (-joint_angle + 120) # 0 degrees when the servos are at 180 deg
#             ARM_MIN = 90
#             ARM_MAX = 165
#
#             if joint_angle_offset < ARM_MIN: 
#                 joint_angle_offset = ARM_MIN
#             elif joint_angle_offset > ARM_MAX: 
#                 joint_angle_offset = ARM_MAX
#             else: 
#                 pass
#
#             self.set_profile_time(joint_id, time)
#             joint_angle_offset  = int((joint_angle_offset) * 4095 / 360) # add the effect of the gear ratio
#             set_position([self.servos[1]], [joint_angle_offset])
#             # set_position([self.servos[1]], [1100])
#
#             joint_angle_camera = -(joint_angle) + 180
#             joint_angle_camera = int((joint_angle_camera) * 4095 / 360) # no offset
#             set_position([self.servos[2]], [joint_angle_camera])
#
#         else: 
#             return
#
#     def set_profile_time(self, joint, time):
#         VEL_PROFILE_ADDR = 112
#         port_handler = self.servos[joint].port_handler
#         packet_handler = self.servos[joint].packet_handler
#         packet_handler.write4ByteTxRx(port_handler, self.ids[joint], VEL_PROFILE_ADDR, time)
#
#     @staticmethod
#     def _cosines_law(l1, l2, opposite_l):
#         return np.arccos((l1**2 + l2**2 - opposite_l**2)/(2*l1*l2))
#
#
#     def handle_input(self, key_1, key_2, key_3):
#
#         if key_1: # move vertical axis joint (arm base joint)
#             self.move_arm_joints(joint_id=0, joint_angle=0)
#             pass
#         else:
#             pass
#
#         if key_2: # move arm joint (arm joint)
#             self.move_arm_joints(joint_id=1, joint_angle=0)
#             pass
#         else:
#             pass
#
#         if key_3: # move camera joint
#             self.move_arm_joints(joint_id=2, joint_angle=0)
#             pass
#         else:
#             pass
#
#
# arm = Arm()
# # arm.set_profile_time(joint=1, time=4000)
# arm.move_arm_joints(joint_id=1, joint_angle=-25, time=4000)
#
# # arm.move_arm_joints(joint_id=1, joint_angle=0, time=2000)
#
# # arm.move_arm_joints(joint_id=2, joint_angle=0, time=2000)
#
#
#
#
#
#
#
#
#
