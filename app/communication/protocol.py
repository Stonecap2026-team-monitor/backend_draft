# app/communication/protocol.py


# ============================================================
# FRAME CONFIG
# ============================================================

START = 0xAA
END = 0x55

MAX_DATA_LENGTH = 16


# ============================================================
# Python -> STM32
# ============================================================

MSG_HEARTBEAT = 0x01

MSG_SET_TARGET = 0x10
MSG_SET_HOME = 0x11
MSG_MOVE_HOME = 0x12
MSG_JOG = 0x13
MSG_CLEAR_ERROR = 0x14


# ============================================================
# STM32 -> Python
# ============================================================

MSG_ACK = 0x80
MSG_STATUS = 0x81
MSG_COMMAND_DONE = 0x82
MSG_ERROR = 0x83
MSG_CURRENT_ANGLE = 0x84
MSG_CURRENT_COMMAND_ANGLES = 0x85
MSG_READY = 0x86


# ============================================================
# JOG AXIS
# ============================================================

AXIS_THETA1 = 1
AXIS_THETA2 = 2
AXIS_THETA3 = 3


# ============================================================
# COMMAND NAME
# ============================================================

COMMAND_NAMES = {
    MSG_HEARTBEAT: "HEARTBEAT",
    MSG_SET_TARGET: "SET_TARGET",
    MSG_SET_HOME: "SET_HOME",
    MSG_MOVE_HOME: "MOVE_HOME",
    MSG_JOG: "JOG",
    MSG_CLEAR_ERROR: "CLEAR_ERROR",
}


# ============================================================
# ERROR NAME
# ============================================================

ERROR_NAMES = {
    0x00: "NONE",
    0x01: "INVALID_TARGET",
    0x02: "INVALID_AXIS",
    0x03: "ANGLE_LIMIT",
    0x04: "STEPPER_BUSY",
    0x05: "STEPPER",
    0x06: "SERVO2",
    0x07: "SERVO3",
    0x08: "HOME_NOT_SET",
    0x09: "INIT",
    0x0A: "QUEUE",
    0x0B: "INVALID_COMMAND",
    0x0C: "COMM_LOST",
    0x0D: "ENCODER",
    0x0E: "SYSTEM_LOCKED",
    0x0F: "ESTOP",
}


# ============================================================
# CHECKSUM
# ============================================================

def calculate_checksum(
    msg_id: int,
    data: bytes
) -> int:

    checksum = msg_id ^ len(data)

    for byte in data:
        checksum ^= byte

    return checksum & 0xFF


# ============================================================
# FRAME BUILD
# ============================================================

def build_frame(
    msg_id: int,
    data: bytes = b""
) -> bytes:

    if not 0 <= msg_id <= 0xFF:
        raise ValueError(
            "msg_id must be 0~255"
        )

    if len(data) > MAX_DATA_LENGTH:
        raise ValueError(
            f"data length exceeds "
            f"MAX_DATA_LENGTH({MAX_DATA_LENGTH})"
        )

    frame = bytearray()

    frame.append(START)
    frame.append(msg_id)
    frame.append(len(data))

    frame.extend(data)

    frame.append(
        calculate_checksum(
            msg_id,
            data
        )
    )

    frame.append(END)

    return bytes(frame)