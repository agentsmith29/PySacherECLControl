from LaserControl.controller.LaserControlErrors import LaserNotConnectedError


class ErrorConverter:

    #@staticmethod
    def convert(msg, additional_message=""):

        msg = msg.replace('>>>>>>>>>>>>>>>>>>>>  ', '').strip()

        if "Fails to open" in msg and "Please check if USB is connected" in msg:
            if additional_message is not None or additional_message != "":
                raise LaserNotConnectedError(f"{msg}. {additional_message}")
            else:
                raise LaserNotConnectedError(f"{msg}")
        else:
            return msg
