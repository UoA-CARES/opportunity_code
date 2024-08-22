from cares_lib.dynamixel.Servo import Servo
from cares_lib.dynamixel.Servo import addresses
import dynamixel_sdk as dxl
from util import (
    set_velocity, 
    set_position,
    _forward_velocity,
    _backward_velocity,
    _left_velocity,
    _right_velocity)
import keyboard
import time
from xbox_controller import XboxController

def main():
    #Parameters
    port = "/dev/ttyUSB0"
    baudrate = 1000000
    max = 4095
    min = 0

    models = input("Enter models for Servos (e.g. MX-106 XL-320): ").split(" ")
    servo_ids = [1, 2]

    protocols = [2] * len(models)
    for i in range(len(models)):
        if models[i][:2] in ["MX", "AX"]:
            protocols[i] = 1

    servo_init_info = {}
    for servo_id, model, protocol in zip(servo_ids, models, protocols):
        servo_init_info[servo_id] = (model, protocol)
    servos = init_servo(port, baudrate, max, min, servo_init_info)
    _display_servos(servos)

    list_of_servos = []
    for i in servos.values():
        list_of_servos.append(i)

    # Velocity Input Range is 0->500 for CCW and 1024->1524 for CW
    standard_velocity = input("Set a standard velocity for Servos (e.g. 200): ")
    standard_velocity = int(standard_velocity)
    joy = XboxController()

    e_stop = True

    while True:
        velocities = [0] * len(servo_ids)

        control_inputs = joy.read()

        left_joy_x, left_joy_y, right_trigger, left_trigger, A_button = control_inputs
        left_joy_x = round(left_joy_x, 1)

        # if not abs(left_joy_x) < 0.1 and abs(left_joy_y) < 0.1:

        #     if abs(left_joy_y) > abs(left_joy_x):
        #         velocities[0] = standard_velocity * right_trigger * left_joy_y / abs(left_joy_y)
        #         velocities[1] = standard_velocity * right_trigger * left_joy_y / abs(left_joy_y)
        #     else:
        #         velocities[0] = standard_velocity * right_trigger * left_joy_x / abs(left_joy_x)
        #         velocities[1] = standard_velocity * right_trigger * left_joy_x / abs(left_joy_x)
    
        # #To drive
        if A_button > 0:
            if e_stop == True:
                e_stop = False
            else:
                e_stop = True
            velocities = [0,0]
        
        if e_stop == False:
            if right_trigger > 0.1:
                val = round(500 * right_trigger/1)
                velocities = _forward_velocity(val)
            if left_trigger > 0.1:
                val = round(500 * left_trigger/1)
                velocities = _backward_velocity(val)
            if left_joy_x > 0.5:
                velocities = _left_velocity(standard_velocity)
            if left_joy_x < -0.5: 
                velocities = _right_velocity(standard_velocity)
        else:
            velocities = [0,0]
        # #To rotate mast
        # if keyboard.is_pressed('q'):
        #     velocities[1] = standard_velocity
        # if keyboard.is_pressed('e'):
        #     velocities[1] = -standard_velocity
        # print(velocities)
        set_velocity(list_of_servos, velocities)
        time.sleep(0.01)

def init_servo(port, baudrate, max, min, servo_init_info) -> dict[int, Servo]:
    servos = {}
    port_handler = dxl.PortHandler(port)

    if not port_handler.openPort():
        error_message = f"Failed to open port"
        raise IOError(error_message)
    
    if not port_handler.setBaudRate(baudrate):
        error_message = f"Failed to change the baudrate"
        raise IOError(error_message)
    
    for servo_id, model_and_protocol in servo_init_info.items():
        model = model_and_protocol[0]
        protocol = model_and_protocol[1]
        packet_handler = dxl.PacketHandler(protocol)
        servos[servo_id] = Servo(
            port_handler,
            packet_handler,
            protocol,
            servo_id,
            1,
            1023,
            1023,
            max,
            min,
            model
            )
        
    return servos

def _display_servos(servos: dict[int, Servo]):
    for id, Servo in servos.items():
        print(f"id({id}) is initialised with model({Servo.model}) and protocol({Servo.protocol})")

# def move_velocity(servos, velocity):
#     portHandler = servos[1].port_handler
#     packetHandler = servos[1].packet_handler
#     servo_ids = list(servos.keys())
#     groupSyncWrite = dxl.GroupSyncWrite(portHandler, packetHandler, addresses["MX-106"]["moving_speed"], addresses["MX-106"]["moving_speed_length"])
#     for ids, data in zip(servo_ids,velocity):
#         print(data)
#         data = decimal_to_hex(data)
#         data = [int(data[2:], 16), int(data[:2], 16)]
#         dxl_addparam_result = groupSyncWrite.addParam(ids, data)
#         if not dxl_addparam_result:
#             print(f"Failed to add parameter for Dynamixel ID {servo_ids[0]}")
#             quit()
#     dxl_comm_result = groupSyncWrite.txPacket()
#     if dxl_comm_result != dxl.COMM_SUCCESS:
#         print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#     groupSyncWrite.clearParam()

# def decimal_to_hex(decimal):
#     hex_value = '{:04X}'.format(decimal & ((1 << 16)-1))
#     return hex_value

if __name__ == "__main__":
    main()