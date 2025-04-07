import time
from datetime import timedelta
from control.servo_factory import servo_factory
from control.util import _bulk_write_protocol_one, _bulk_write_protocol_two, set_servo_torque
from cares_lib.dynamixel.Servo import Servo
from cares_lib.dynamixel.Servo import addresses
import dynamixel_sdk as dxl
import random

DYNAMIXEL_MODEL_NAMES = {
    350: "XL-320",
    1060: "XL430-W250-T",
    1020: "XM430-W350",
    321: "MX-106Protocol2", #Protocol 2
    320: "MX-106"  #Protocol 1
}

PORT_NAME = "/dev/ttyMast"

PROTOCOLS = {
    1,
    2
}

PROFILE_VELOCITY = 100

MAX_POSITIONS = {
    3: 1900,     #ID: max
    4: 1200        #1220 is good limt for heaed down tilt but when not powered the servo goes to ~1270
}

MIN_POSITIONS = {
    3: 450,      #ID: min
    4: 1060
}

MOVE_SET = [
    [470,1150],
    [1850,1090],
    [1450,1090],
    [1150,1150],
    [850,1090],
]

MOVE_TIMER = [
    15,             #Determines the range of time between head movements, default is between 15-30 seconds
    30
]

def modelnumtoname(num):
    for number in DYNAMIXEL_MODEL_NAMES:
        if number == num:
            return DYNAMIXEL_MODEL_NAMES[number]
        else:
            continue

def servo_search(port):
    port_handler = dxl.PortHandler(port)
    servos = []
    for protocol in PROTOCOLS:
        print(f"Searching protocol: {protocol}")
        packet_handler = dxl.PacketHandler(protocol)

        if port_handler.openPort():
            print("Succeeded to open the port!")
        else:   
            print("Failed to open the port!")

        if port_handler.setBaudRate(1000000):
            print("Succeeded to change the baudrate!")
        else:
            print("Failed to change the baudrate!")

        
        for dxl_id in range(1,20):
            dxl_model_number, dxl_comm_result, dxl_error = packet_handler.ping(port_handler, dxl_id)
            if dxl_comm_result == dxl.COMM_SUCCESS:
                print(f"ID:{dxl_id} Found Dynamixel model number: {dxl_model_number} as model: {modelnumtoname(dxl_model_number)}")
                servos.append([dxl_id, modelnumtoname(dxl_model_number), protocol])
            elif dxl_comm_result != dxl.COMM_RX_TIMEOUT:
                print(f"ID:{dxl_id} Communication error: {packet_handler.getTxRxResult(dxl_comm_result)}")

        port_handler.closePort()

    if len(servos) == 2:
        print(f"Dynamixels found: {servos}, All servos found")
        return servos
    else:
        return servos



class Mast():
    def __init__(self, max_servo_speed, found_servos):
        """
        Mast class to control the mast of the robot
        :param max_servo_speed: The maximum speed of the servos

        Clockwise tilt is defined as tilting the top part backward
        Counterclockwise tilt is defined as tilting the top part forward
        """
        self.servo_speed = max_servo_speed
        self.servos = []

        # Servos located at the base of the mast and the head, with ids 3 and 4
        for ids, names, protocol in found_servos:
            self.servos.append(
                servo_factory.create_servo(
                    model=names,
                    port=PORT_NAME,
                    protocol=protocol,
                    baudrate=1000000,
                    # head servo needs to be limited to a range of motion of 90 degrees
                    max=4095 if protocol == 1 else 4095,
                    min=0,
                    id=ids,
                )
            )

        for servo in self.servos:
            servo.packet_handler.write1ByteTxRx(servo.port_handler, servo.motor_id, 64, 1)
            dxl_comm_result, dxl_error = servo.packet_handler.write4ByteTxRx(servo.port_handler, servo.motor_id, 112, 1000)
            time.sleep(1)
            dxl_profile_velo, dxl_comm_result, dxl_error = servo.packet_handler.read4ByteTxRx(servo.port_handler, servo.motor_id, 112)
            print(dxl_profile_velo)


    def verify_postion(self, servo, position):
        current_position = self.get_servo_position(servo)
        print("Current", current_position)
        if current_position[0] > MAX_POSITIONS[servo.motor_id] or current_position[0] < MIN_POSITIONS[servo.motor_id]:
            print("servo out of bounds, please re-centre")
            return False
        elif position > MAX_POSITIONS[servo.motor_id] or position < MIN_POSITIONS[servo.motor_id]:
            print("attempted to move out of bounds")
            return False
        else:
            return True
                
    
    def positionmove_sameprotocol(self, positions):
        group_position = []
        group_servos = []
        #Verify positions are within bounds
        for position,servo in zip(positions, self.servos):
                self.set_profile_velocity(servo)
            # if not self.verify_postion(servo, position):
            #     raise ValueError(f"Servo position, {position} is out of servo {servo.motor_id} bounds")
            # else:
                group_position.append(position)
                group_servos.append(servo)
        # Based on the address jsons from cares_lib
        # address = addresses[group_servos[0].model]["goal_position"]
        address = 116
        # address_length = addresses[group_servos[0].model]["goal_position_length"]
        address_length = 4

        # All servos of the same model should have the same
        # port handler, packet handler and protocol
        port_handler = group_servos[0].port_handler
        packet_handler = group_servos[0].packet_handler
        protocol = group_servos[0].protocol


        # Bulk Write to Servos
        _bulk_write_protocol_two(group_servos, group_position, port_handler, packet_handler, address, address_length)

                

    def get_servo_position(self, servo):
        """
        Get the positions of the servos
        Args:
            servos: list(Servo) - list of servos to get positions from
        """
        dxl_current_position, dxl_comm_result, dxl_error = servo.packet_handler.read4ByteTxRx(servo.port_handler, servo.motor_id, 132)
        return [dxl_current_position]

    def set_profile_velocity(self, servo):
        """
        Sets the profile velocity for an individual servo. (requires protocol 2)
        """
        dxl_comm_result, dxl_error = servo.packet_handler.write4ByteTxRx(servo.port_handler, servo.motor_id, 112, PROFILE_VELOCITY)
        return
        
        
def main():
    time.sleep(5)
    servos = servo_search(PORT_NAME)
    if len(servos) < 2:
        print("Failed to find servos")
        raise ValueError(f"Incorrect number of servos detected, #Servos Detected: {len(servos)}, should be 2, check power and restart")
    else:
        mast = Mast(20,servos)
    
    # MAIN LOOP
    current_positions = [0,0]
    while True:
        #Random Sampling
        positions = random.sample(MOVE_SET, 1)[0]
        while positions == current_positions:
            positions = random.sample(MOVE_SET,1)[0]
        print("Positions: " ,positions)
        mast.positionmove_sameprotocol(positions)       #Sample a Random Position
        wait_time = random.randint(MOVE_TIMER[0],MOVE_TIMER[1])
        end_time = time.time() + wait_time

        while time.time() <= end_time:
            remaining_time = int(end_time - time.time())
            formatted_time = str(timedelta(seconds=remaining_time))
            print("Until Next Move: ", formatted_time, end='\r', flush=True)
            time.sleep(1)
        print("00:00:00")
        current_positions = positions


if __name__ == "__main__":
    main()
