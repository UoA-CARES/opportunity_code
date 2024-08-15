from cares_lib.dynamixel.Servo import Servo
import dynamixel_sdk as dxl

class ServoFactory:
    def __init__(self):
        self.last_servo_id = 0

    def create_servo(self, model, port, protocol, baudrate, max, min) -> Servo:
        
        port_handler = dxl.PortHandler(port)
        packet_handler = dxl.PacketHandler(protocol)

        if not port_handler.openPort():
            error_message = f"Failed to open port"
            raise IOError(error_message)

        if not port_handler.setBaudRate(baudrate):
            error_message = f"Failed to change the baudrate"
            raise IOError(error_message)
        
        self.last_servo_id += 1

        return Servo(
            port_handler,
            packet_handler,
            protocol,
            self.last_servo_id,
            1,
            1023,
            1023,
            max,
            min,
            model,
        )
        
servo_factory = ServoFactory()