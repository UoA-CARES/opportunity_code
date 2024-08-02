from cares_lib.dynamixel.Servo import Servo
from cares_lib.dynamixel.Servo import addresses
import dynamixel_sdk as dxl
import cv2 as cv
import numpy as np


def main():
    #Parameters
    port = "/dev/ttyUSB2"
    protocol = 1
    baudrate = 1000000
    servo_ids = [1, 2]
    max = 4095
    min = 0
    model = "MX-106"
    servos = init_servo(port, protocol, baudrate, servo_ids, max, min, model)
    print("Servos Initialized")

    while True:
        # Velocity Input Range is 0->500 for CCW and 1024->1524 for CW
        velocity = input("Enter velocity for Servos (e.g. 200,300): ").split(" ")
        # Conversion of list of str to list of int
        velocity = [int(num) for num in velocity]
        if any(num > 500 for num in velocity) or any(num < -500 for num in velocity):
            print("Invalid velocity")
        else: 
            for i in range(len(velocity)):
                if velocity[i] < 0:
                    velocity[i] = abs(velocity[i]) + 1024
            move_velocity(servos, velocity)
            
          
    
    
def init_servo(port, protocol, baudrate, servo_ids, max, min, model):
    servo = {}
    port_handler = dxl.PortHandler(port)
    packet_handler = dxl.PacketHandler(protocol)
    
    if not port_handler.openPort():
        error_message = f"Failed to open port"
        raise IOError(error_message)
    
    if not port_handler.setBaudRate(baudrate):
        error_message = f"Failed to change the baudrate"
        raise IOError(error_message)
    for ids in servo_ids:
        servo[ids] = Servo(
            port_handler,
            packet_handler,
            protocol,
            ids,
            1,
            1023,
            1023,
            max,
            min,
            model
            )
    
    return servo

def move_velocity(servos, velocity):
    portHandler = servos[1].port_handler
    packetHandler = servos[1].packet_handler
    servo_ids = list(servos.keys())

    groupSyncWrite = dxl.GroupSyncWrite(portHandler, packetHandler, addresses["MX-106"]["moving_speed"], addresses["MX-106"]["moving_speed_length"])
    for ids, data in zip(servo_ids,velocity):
        print(data)
        data = decimal_to_hex(data)
        data = [int(data[2:], 16), int(data[:2], 16)]
        dxl_addparam_result = groupSyncWrite.addParam(ids, data)
        if not dxl_addparam_result:
            print(f"Failed to add parameter for Dynamixel ID {servo_ids[0]}")
            quit()

    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    groupSyncWrite.clearParam()

def decimal_to_hex(decimal):
    hex_value = '{:04X}'.format(decimal & ((1 << 16)-1))
    return hex_value
    
if __name__ == "__main__":
    main()