import serial


SERIAL_PORT = "/dev/ttyTHS1"
BAUDRATE = 115200


def open_serial():
    return serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,
    )


def build_jog_data(axis: int, delta_deg: float) -> bytes:
    delta_x10 = int(delta_deg * 10)

    axis_byte = axis.to_bytes(
        1,
        byteorder="big",
        signed=False,
    )

    delta_bytes = delta_x10.to_bytes(
        2,
        byteorder="big",
        signed=True,
    )

    return axis_byte + delta_bytes




def send_jog(serial_port, axis: int, delta_deg: float):
    data = build_jog_data(axis, delta_deg)

    serial_port.write(data)
    serial_port.flush()

    return data