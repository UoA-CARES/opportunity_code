from cares_lib.dynamixel.Servo import Servo
import dynamixel_sdk as dxl

class ServoFactory:
    
    def create_servo(self, model, port, protocol, baudrate, max, min, id) -> Servo:
        
        port_handler = dxl.PortHandler(port)
        packet_handler = dxl.PacketHandler(protocol)

        if not port_handler.openPort():
            error_message = f"Failed to open port"
            raise IOError(error_message)

        if not port_handler.setBaudRate(baudrate):
            error_message = f"Failed to change the baudrate"
            raise IOError(error_message)

        return Servo(
            port_handler,
            packet_handler,
            protocol,
            id,
            1,
            1023,
            1023,
            max,
            min,
            model,
        )
        
servo_factory = ServoFactory()