from cares_lib.dynamixel.Servo import Servo
from cares_lib.dynamixel.Servo import addresses
import dynamixel_sdk as dxl
import cv2 as cv
import numpy as np
from util import set_velocity, set_position


def main():
    #Parameters
    port = "/dev/ttyUSB2"
    baudrate = 1000000
    max = 4095
    min = 0
    
    models = input("Enter models for Servos (e.g. MX-106 XL-320): ").split(" ")
    servo_ids = list(range(1, len(models)+1))

    protocols = [2] * len(models)
    for i in range(len(models)):
        if models[i][:2] in ["MX", "AX"]:
            protocols[i] = 1
    
    servo_init_info = {}
    for servo_id, model, protocol in zip(servo_ids, models, protocols):
        servo_init_info[servo_id] = (model, protocol)

    servos = init_servo(port, baudrate, max, min, servo_init_info)
    _display_servos(servos)

    positions = [0]*len(models)

    # Velocity Input Range is 0->500 for CCW and 1024->1524 for CW
    velocities = input("Enter velocity for Servos (e.g. 200 300): ").split(" ")
    # Conversion of list of str to list of int
    velocities = [int(velocity) for velocity in velocities]
    set_velocity(servos, velocities)

    # Moving servos simultaneously
    while True:
        increment = input("To move servos, enter a for CCW, d for CW: ")
        if increment == 'd':
            positions = [ i+10 for i in positions]
        if increment == 'a':
            positions = [ i-10 for i in positions]
        print(f"Current position at {positions[0]}")
        set_position(servos, positions)

          
    
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