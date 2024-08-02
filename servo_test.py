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
        # Velocity Input Range is 0->1023 for CCW and 1024->2047 for CW
        velocity = int(input("Enter velocity: "))
        if velocity < 0 or velocity > 2047 or velocity == None:
            print("Invalid velocity")
        else: 
            move_velo(servos, velocity)
            
          
    
    
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

def move_velo(servos, velocity):
    portHandler = servos[1].port_handler
    packetHandler = servos[1].packet_handler
    motor_ids = list(servos.keys())

    # Velocity input must be a converted hex number
    velocity = decimal_to_hex(velocity)
    print(velocity)
    data = [int(velocity[2:], 16), int(velocity[:2], 16)]
    print(data)
    groupSyncWrite = dxl.GroupSyncWrite(portHandler, packetHandler, addresses["MX-106"]["moving_speed"], addresses["MX-106"]["moving_speed_length"])
    for ids in motor_ids:
        dxl_addparam_result = groupSyncWrite.addParam(ids, data)
        if not dxl_addparam_result:
            print(f"Failed to add parameter for Dynamixel ID {motor_ids[0]}")
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