class STM32Simulator:

    def __init__(self):

        self.current_theta1_deg = 0.0
        self.current_theta2_deg = 0.0
        self.current_theta3_deg = 0.0

        self.home_theta1_deg = 0.0
        self.home_theta2_deg = 0.0
        self.home_theta3_deg = 0.0

        self.last_command_error_code = None
        self.last_command_error_name = None


    def start(self):
        print("STM32 SIMULATOR STARTED")


    def close(self):
        print("STM32 SIMULATOR CLOSED")


    def jog(self, axis, delta_deg):

        if axis == 1:
            self.current_theta1_deg += delta_deg

        elif axis == 2:
            self.current_theta2_deg += delta_deg

        elif axis == 3:
            self.current_theta3_deg += delta_deg

        else:
            return False


        print(
            "SIMULATOR CURRENT ANGLES : "
            f"theta1={self.current_theta1_deg:+.1f}, "
            f"theta2={self.current_theta2_deg:+.1f}, "
            f"theta3={self.current_theta3_deg:+.1f}"
        )

        return True


    def set_home(self):

        self.home_theta1_deg = self.current_theta1_deg
        self.home_theta2_deg = self.current_theta2_deg
        self.home_theta3_deg = self.current_theta3_deg

        print(
            "SIMULATOR HOME SAVED : "
            f"theta1={self.home_theta1_deg:+.1f}, "
            f"theta2={self.home_theta2_deg:+.1f}, "
            f"theta3={self.home_theta3_deg:+.1f}"
        )

        return True


    def move_home(self):

        self.current_theta1_deg = self.home_theta1_deg
        self.current_theta2_deg = self.home_theta2_deg
        self.current_theta3_deg = self.home_theta3_deg

        print(
            "SIMULATOR MOVED HOME : "
            f"theta1={self.current_theta1_deg:+.1f}, "
            f"theta2={self.current_theta2_deg:+.1f}, "
            f"theta3={self.current_theta3_deg:+.1f}"
        )

        return True


    def clear_error(self):

        self.last_command_error_code = None
        self.last_command_error_name = None

        print("SIMULATOR ERROR CLEARED")

        return True