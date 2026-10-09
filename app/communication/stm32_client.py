# app/communication/stm32_client.py

import serial
import struct
import threading
import time

from .protocol import (
    START,
    END,
    MAX_DATA_LENGTH,

    MSG_HEARTBEAT,

    MSG_SET_TARGET,
    MSG_SET_HOME,
    MSG_MOVE_HOME,
    MSG_JOG,
    MSG_CLEAR_ERROR,

    MSG_ACK,
    MSG_STATUS,
    MSG_COMMAND_DONE,
    MSG_ERROR,
    MSG_CURRENT_ANGLE,
    MSG_CURRENT_COMMAND_ANGLES,
    MSG_READY,

    AXIS_THETA1,
    AXIS_THETA2,
    AXIS_THETA3,

    COMMAND_NAMES,
    ERROR_NAMES,

    calculate_checksum,
    build_frame,
)


class STM32Client:

    def __init__(
        self,
        port: str,
        baud: int = 115200
    ):
        self.port = port
        self.baud = baud

        self.ser = None

        self.write_lock = threading.Lock()
        # 紐⑦꽣 紐낅졊�� �숈떆�� �섎굹留� �ㅽ뻾
        self.command_lock = threading.Lock()
        # COMMAND_DONE / ERROR ��湲곗슜
        self.command_done_event = threading.Event()
        self.command_error_event = threading.Event()

        # �꾩옱 �꾨즺瑜� 湲곕떎由щ뒗 紐낅졊
        self.expected_command_id = None

        # �꾩옱 紐낅졊�먯꽌 諛쒖깮�� �먮윭
        self.last_command_error_code = None
        self.last_command_error_name = None

        self.stop_event = threading.Event()

        self.rx_thread = None
        self.heartbeat_thread = None

        self.heartbeat_enabled = True
        self.alive_counter = 0

        # ----------------------------------------------------
        # STM32 �곹깭
        # ----------------------------------------------------

        self.ready = False

        self.last_error_code = None
        self.last_error_name = None

        self.encoder_angle_deg = None

        self.current_theta1_deg = None
        self.current_theta2_deg = None
        self.current_theta3_deg = None


    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.ser is not None and self.ser.is_open:
            print("STM32 serial already opened")
            return

        self.stop_event.clear()

        self.ser = serial.Serial(
            self.port,
            self.baud,
            timeout=0.1,
            write_timeout=1.0
        )

        print(
            f"STM32 Serial Open : "
            f"{self.port} / {self.baud}"
        )

        # 湲곗〈 �뚯뒪�� 肄붾뱶�먯꽌 �ъ슜�� �덉젙�� �쒓컙 �좎�
        time.sleep(2.0)

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()


        # ----------------------------------------------------
        # RX THREAD
        # ----------------------------------------------------

        self.rx_thread = threading.Thread(
            target=self._receive_loop,
            daemon=True
        )

        self.rx_thread.start()


        # ----------------------------------------------------
        # HEARTBEAT THREAD
        # ----------------------------------------------------

        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )

        self.heartbeat_thread.start()


    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        self.stop_event.set()

        if self.ser is not None:

            if self.ser.is_open:
                self.ser.close()

        print(
            "STM32 Serial Closed"
        )


    # ========================================================
    # SAFE UART WRITE
    # ========================================================

    def _safe_write(
        self,
        frame: bytes
    ):

        if self.ser is None:
            raise RuntimeError(
                "STM32 serial is not started"
            )

        if not self.ser.is_open:
            raise RuntimeError(
                "STM32 serial port is closed"
            )

        with self.write_lock:

            self.ser.write(
                frame
            )

            self.ser.flush()

    # ========================================================
    # EXECUTE COMMAND
    # ========================================================

    def _execute_command(
        self,
        command_id: int,
        frame: bytes,
        timeout_sec: float
    ) -> bool:

        with self.command_lock:

            self.command_done_event.clear()
            self.command_error_event.clear()

            self.last_command_error_code = None
            self.last_command_error_name = None

            self.expected_command_id = command_id

            try:

                self._safe_write(
                    frame
                )

                start_time = time.monotonic()

                while True:

                    # -----------------------------------------
                    # COMMAND_DONE �섏떊
                    # -----------------------------------------

                    if self.command_done_event.is_set():

                        return True


                    # -----------------------------------------
                    # ERROR �섏떊
                    # -----------------------------------------

                    if self.command_error_event.is_set():

                        return False


                    # -----------------------------------------
                    # �꾨줈洹몃옩 醫낅즺
                    # -----------------------------------------

                    if self.stop_event.is_set():

                        return False


                    # -----------------------------------------
                    # TIMEOUT
                    # -----------------------------------------

                    if (
                        time.monotonic()
                        - start_time
                        >= timeout_sec
                    ):

                        print(
                            f"COMMAND TIMEOUT : "
                            f"{COMMAND_NAMES.get(command_id, hex(command_id))}"
                        )

                        return False


                    time.sleep(0.01)

            finally:

                self.expected_command_id = None


    # ========================================================
    # HEARTBEAT
    # ========================================================

    def _heartbeat_loop(self):

        while not self.stop_event.is_set():

            if (
                self.ser is None
                or not self.ser.is_open
            ):
                break


            if self.heartbeat_enabled:

                self.alive_counter = (
                    self.alive_counter + 1
                ) & 0xFF


                data = bytes(
                    [self.alive_counter]
                )


                frame = build_frame(
                    MSG_HEARTBEAT,
                    data
                )


                try:

                    self._safe_write(
                        frame
                    )

                except (
                    serial.SerialException,
                    RuntimeError
                ) as exc:

                    print(
                        f"HEARTBEAT ERROR : {exc}"
                    )

                    break


            time.sleep(1.0)


    # ========================================================
    # SET_TARGET
    # ========================================================

    def set_target(
        self,
        theta1_deg: float,
        theta2_deg: float,
        theta3_deg: float
    ):

        theta1_x10 = int(
            round(theta1_deg * 10.0)
        )

        theta2_x10 = int(
            round(theta2_deg * 10.0)
        )

        theta3_x10 = int(
            round(theta3_deg * 10.0)
        )


        data = struct.pack(
            ">hhh",
            theta1_x10,
            theta2_x10,
            theta3_x10
        )


        frame = build_frame(
            MSG_SET_TARGET,
            data
        )


        print(
            f"SET_TARGET TX : "
            f"theta1={theta1_deg:+.1f}, "
            f"theta2={theta2_deg:+.1f}, "
            f"theta3={theta3_deg:+.1f}"
        )

        return self._execute_command(
            MSG_SET_TARGET,
            frame,
            timeout_sec=90.0
        )


    # ========================================================
    # JOG
    # ========================================================

    def jog(
        self,
        axis: int,
        delta_deg: float
    ):

        if axis not in (
            AXIS_THETA1,
            AXIS_THETA2,
            AXIS_THETA3
        ):

            raise ValueError(
                "axis must be 1, 2 or 3"
            )


        delta_x10 = int(
            round(delta_deg * 10.0)
        )


        data = bytearray()

        data.append(
            axis
        )


        data.extend(
            struct.pack(
                ">h",
                delta_x10
            )
        )


        frame = build_frame(
            MSG_JOG,
            bytes(data)
        )


        print(
        f"JOG TX : "
        f"axis={axis}, "
        f"delta={delta_deg:+.1f} deg"
        )

        return self._execute_command(
            MSG_JOG,
            frame,
            timeout_sec=10.0
        )


    # ========================================================
    # SET_HOME
    # ========================================================

    def set_home(self) -> bool:

        frame = build_frame(
            MSG_SET_HOME
        )

        print(
            "SET_HOME TX"
        )

        return self._execute_command(
            MSG_SET_HOME,
            frame,
            timeout_sec=5.0
        )


    # ========================================================
    # MOVE_HOME
    # ========================================================

    def move_home(self) -> bool:

        frame = build_frame(
            MSG_MOVE_HOME
        )

        print(
            "MOVE_HOME TX"
        )

        return self._execute_command(
            MSG_MOVE_HOME,
            frame,
            timeout_sec=90.0
        )

    # ========================================================
    # CLEAR_ERROR
    # ========================================================

    def clear_error(self) -> bool:

        frame = build_frame(
            MSG_CLEAR_ERROR
        )

        print(
            "CLEAR_ERROR TX"
        )

        return self._execute_command(
            MSG_CLEAR_ERROR,
            frame,
            timeout_sec=5.0
        )


    # ========================================================
    # HEARTBEAT CONTROL
    # ========================================================

    def enable_heartbeat(self):

        self.heartbeat_enabled = True

        print(
            "HEARTBEAT ON"
        )


    def disable_heartbeat(self):

        self.heartbeat_enabled = False

        print(
            "HEARTBEAT OFF"
        )


    # ========================================================
    # RX LOOP
    # ========================================================

    def _receive_loop(self):

        try:

            while not self.stop_event.is_set():

                if (
                    self.ser is None
                    or not self.ser.is_open
                ):
                    break


                # ------------------------------------------------
                # START
                # ------------------------------------------------

                start = self.ser.read(1)

                if len(start) == 0:
                    continue


                if start != bytes([START]):
                    continue


                # ------------------------------------------------
                # MSG_ID + LENGTH
                # ------------------------------------------------

                header = self.ser.read(2)

                if len(header) != 2:

                    print(
                        "RX HEADER LENGTH ERROR"
                    )

                    continue


                msg_id = header[0]
                length = header[1]


                if length > MAX_DATA_LENGTH:

                    print(
                        f"RX DATA LENGTH INVALID : "
                        f"{length}"
                    )

                    continue


                # ------------------------------------------------
                # DATA
                # ------------------------------------------------

                data = self.ser.read(
                    length
                )


                if len(data) != length:

                    print(
                        f"RX DATA LENGTH ERROR : "
                        f"expected={length}, "
                        f"received={len(data)}"
                    )

                    continue


                # ------------------------------------------------
                # CHECKSUM
                # ------------------------------------------------

                rx_checksum = self.ser.read(1)

                if len(rx_checksum) != 1:

                    print(
                        "RX CHECKSUM BYTE ERROR"
                    )

                    continue


                # ------------------------------------------------
                # END
                # ------------------------------------------------

                end = self.ser.read(1)


                if end != bytes([END]):

                    print(
                        "RX END BYTE ERROR"
                    )

                    continue


                # ------------------------------------------------
                # CHECKSUM VERIFY
                # ------------------------------------------------

                calc_checksum = calculate_checksum(
                    msg_id,
                    data
                )


                if (
                    calc_checksum
                    != rx_checksum[0]
                ):

                    print(
                        f"RX CHECKSUM ERROR : "
                        f"RX=0x{rx_checksum[0]:02X}, "
                        f"CALC=0x{calc_checksum:02X}"
                    )

                    continue


                # ------------------------------------------------
                # Valid Frame
                # ------------------------------------------------

                self._handle_frame(
                    msg_id,
                    data
                )


        except serial.SerialException as exc:

            if not self.stop_event.is_set():

                print(
                    f"RX SERIAL ERROR : "
                    f"{exc}"
                )


    # ========================================================
    # FRAME HANDLER
    # ========================================================

    def _handle_frame(
        self,
        msg_id: int,
        data: bytes
    ):

        # ====================================================
        # ACK
        # ====================================================

        if msg_id == MSG_ACK:

            if len(data) != 1:
                return


            ack_id = data[0]


            # Heartbeat ACK�� 異쒕젰�섏� �딆쓬
            if ack_id == MSG_HEARTBEAT:
                print(
                    "ACK : HEARTBEAT (0x01)"
                )
                return


            command_name = COMMAND_NAMES.get(
                ack_id,
                f"UNKNOWN(0x{ack_id:02X})"
            )


            print(
                f"ACK : "
                f"{command_name} "
                f"(0x{ack_id:02X})"
            )


        # ====================================================
        # COMMAND DONE
        # ====================================================

        elif msg_id == MSG_COMMAND_DONE:

            if len(data) != 1:
                return


            completed_id = data[0]


            command_name = COMMAND_NAMES.get(
                completed_id,
                f"UNKNOWN(0x{completed_id:02X})"
            )


            print(
                f"COMMAND DONE : "
                f"{command_name} "
                f"(0x{completed_id:02X})"
            )

            if completed_id == self.expected_command_id:

                self.command_done_event.set()


        # ====================================================
        # ERROR
        # ====================================================

        elif msg_id == MSG_ERROR:

            if len(data) != 1:
                return


            error_code = data[0]


            self.last_error_code = (
                error_code
            )


            self.last_error_name = (
                ERROR_NAMES.get(
                    error_code,
                    f"UNKNOWN(0x{error_code:02X})"
                )
            )


            print(
                f"STM32 ERROR : "
                f"{self.last_error_name} "
                f"(0x{error_code:02X})"
            )
            if self.expected_command_id is not None:

                self.last_command_error_code = error_code
                self.last_command_error_name = self.last_error_name

                self.command_error_event.set()


        # ====================================================
        # AS5600 ACTUAL THETA1
        # ====================================================

        elif msg_id == MSG_CURRENT_ANGLE:

            if len(data) != 2:
                return


            angle_x10 = struct.unpack(
                ">h",
                data
            )[0]


            self.encoder_angle_deg = (
                angle_x10 / 10.0
            )


            print(
                f"ENCODER ANGLE : "
                f"{self.encoder_angle_deg:+.1f} deg"
            )


        # ====================================================
        # CURRENT COMMAND ANGLES
        # ====================================================

        elif (
            msg_id
            == MSG_CURRENT_COMMAND_ANGLES
        ):

            if len(data) != 6:
                return


            (
                theta1_x10,
                theta2_x10,
                theta3_x10
            ) = struct.unpack(
                ">hhh",
                data
            )


            self.current_theta1_deg = (
                theta1_x10 / 10.0
            )

            self.current_theta2_deg = (
                theta2_x10 / 10.0
            )

            self.current_theta3_deg = (
                theta3_x10 / 10.0
            )


            print(
                f"CURRENT COMMAND ANGLES : "
                f"theta1="
                f"{self.current_theta1_deg:+.1f}, "
                f"theta2="
                f"{self.current_theta2_deg:+.1f}, "
                f"theta3="
                f"{self.current_theta3_deg:+.1f}"
            )


        # ====================================================
        # READY
        # ====================================================

        elif msg_id == MSG_READY:

            if len(data) != 0:
                return


            self.ready = True

            print(
                "STM32 READY"
            )


        # ====================================================
        # STATUS
        # ====================================================

        elif msg_id == MSG_STATUS:

            print(
                "STM32 STATUS :",
                data.hex(" ").upper()
            )


        # ====================================================
        # UNKNOWN
        # ====================================================

        else:

            print(
                f"UNKNOWN STM32 MESSAGE : "
                f"0x{msg_id:02X}"
            )