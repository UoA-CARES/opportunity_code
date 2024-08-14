from cares_lib.dynamixel.Servo import Servo
from cares_lib.dynamixel.Servo import addresses
import dynamixel_sdk as dxl


def set_velocity(servos, velocities):
    """
    Send velocities to the servos

    Args:
        servos: list(Servo) - list of servos to send velocities to
        velocities: list(int) - list of velocities to send to the servos

    Returns:
        None

    Note: servos aren't guaranteed to be the same model or protocol
    Assumption: Servos of the same model use the same protocol
    """

    # Group Servos based on Model
    servos_by_model: dict[str, tuple[Servo, float]] = _sort_servos_by_model(
        servos, velocities
    )

    # Write to Servos
    for model, servos_and_velocities in servos_by_model.items():

        # Unpack Servos and Velocities
        servos, velocities = zip(*servos_and_velocities)

        # Verify velocities are within bounds
        if any(
            abs(velocity) > servo.max_velocity
            for servo, velocity in zip(servos, velocities)
        ):
            raise ValueError("Velocity out of bounds")

        # Based on the address jsons from cares_lib
        address = (
            addresses[model]["moving_speed"]
            if "moving_speed" in addresses[model]
            else addresses[model]["goal_velocity"]
        )
        address_length = (
            addresses[model]["moving_speed_length"]
            if "moving_speed_length" in addresses[model]
            else addresses[model]["goal_velocity_length"]
        )

        # All servos of the same model should have the same
        # port handler, packet handler and protocol
        port_handler = servos[0].port_handler
        packet_handler = servos[0].packet_handler
        protocol = servos[0].protocol

        # Bulk Write to Servos
        if protocol == 1:
            _bulk_write_protocol_one(
                servos,
                velocities,
                port_handler,
                packet_handler,
                address,
                address_length,
            )
        elif protocol == 2:
            _bulk_write_protocol_two(
                servos,
                velocities,
                port_handler,
                packet_handler,
                address,
                address_length,
            )
        else:
            raise ValueError(f"Protocol {protocol} not supported")


def set_position(servos, positions):
    """
    Send positions to the servos

    Args:
        servos: list(Servo) - list of servos to send positions to
        positions: list(int) - list of positions to send to the servos. This is bound between max/min

    Returns:
        None

    Note: servos aren't guaranteed to be the same model
    Assumption: Servos of the same model use the same protocol
    """

    # Group Servos based on Model
    servos_by_model: dict[str, tuple[Servo, float]] = _sort_servos_by_model(
        servos, positions
    )

    # Write to Servos
    for model, servos_and_positions in servos_by_model.items():

        # Unpack Servos and Positions
        servos, positions = zip(*servos_and_positions)

        # Verify positions are within bounds
        if any(
            position < servo.min or position > servo.max
            for servo, position in zip(servos, positions)
        ):
            raise ValueError("Position out of bounds")

        # Based on the address jsons from cares_lib
        address = addresses[model]["goal_position"]
        address_length = addresses[model]["goal_position_length"]

        # All servos of the same model should have the same
        # port handler, packet handler and protocol
        port_handler = servos[0].port_handler
        packet_handler = servos[0].packet_handler
        protocol = servos[0].protocol

        # Bulk Write to Servos
        if protocol == 1:
            _bulk_write_protocol_one(
                servos, positions, port_handler, packet_handler, address, address_length
            )
        elif protocol == 2:
            _bulk_write_protocol_two(
                servos, positions, port_handler, packet_handler, address, address_length
            )
        else:
            raise ValueError(f"Protocol {protocol} not supported")


def _sort_servos_by_model(servos: list[Servo], payloads: list[float]):
    """
    Sort the servos by model

    Args:
        servos: list(Servo) - list of servos to sort
        payloads: list(float) - list of payloads to eventually send to the servos

    Returns:
        servos_by_model: dict(str, list(tuple(Servo, float))) - dictionary of tuples of servos and payloads sorted by model
    """
    servos_by_model = {}

    for servo, data in zip(servos, payloads):
        model = servo.model

        if model not in servos_by_model:
            servos_by_model[model] = []

        servos_by_model[model].append((servo, data))

    return servos_by_model


def _bulk_write_protocol_one(
    servos: list[Servo],
    payloads: list[float],
    port_handler,
    packet_handler,
    address,
    address_length,
):
    """
    Bulk write to servos using protocol one

    Args:
        servos: list(Servo) - list of servos to send velocities to
        payloads: list(float) - list of payloads to send to the servos
        port_handler: PortHandler - port handler to use for communication
        packet_handler: PacketHandler - packet handler to use for communication
        address: int - address to write to
        address_length: int - length of the address
    """

    group_sync_write = dxl.GroupSyncWrite(
        port_handler,
        packet_handler,
        address,
        address_length,
    )

    for servo, data in zip(servos, payloads):
        servo_id = servo.motor_id

        data = _decimal_to_hex(data)
        data = [int(data[2:], 16), int(data[:2], 16)]

        dxl_addparam_result = group_sync_write.addParam(servo_id, data)

        if not dxl_addparam_result:
            print(f"Failed to add parameter for Dynamixel ID {servo_id}")
            quit()

    dxl_comm_result = group_sync_write.txPacket()

    if dxl_comm_result != dxl.COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

    group_sync_write.clearParam()


def _bulk_write_protocol_two(
    servos: list[Servo],
    payloads: list[float],
    port_handler,
    packet_handler,
    address,
    address_length,
):
    """
    Bulk write to servos using protocol two

    Args:
        servos: list(Servo) - list of servos to send velocities to
        payloads: list(float) - list of payloads to send to the servos
        port_handler: PortHandler - port handler to use for communication
        packet_handler: PacketHandler - packet handler to use for communication
        address: int - address to write to
        address_length: int - length of the address
    """

    group_bulk_write = dxl.GroupBulkWrite(port_handler, packet_handler)

    for servo, data in zip(servos, payloads):
        servo_id = servo.motor_id

        data = _decimal_to_hex(data)
        data = [int(data[2:], 16), int(data[:2], 16)]

        dxl_addparam_result = group_bulk_write.addParam(
            servo_id, address, address_length, data
        )

        if not dxl_addparam_result:
            print(f"Failed to add parameter for Dynamixel ID {servo_id}")
            quit()

    dxl_comm_result = group_bulk_write.txPacket()

    if dxl_comm_result != dxl.COMM_SUCCESS:
        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

    group_bulk_write.clearParam()


def _decimal_to_hex(decimal):
    hex_value = "{:04X}".format(decimal & ((1 << 16) - 1))
    return hex_value
