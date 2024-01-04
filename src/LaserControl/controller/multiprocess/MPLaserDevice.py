import logging
import os
import time
from multiprocessing import Value
import cmp

from LaserControl.controller.LaserCon import LaserCon


class MPLaserDevice(cmp.CProcess):

    def __init__(self, state_queue, cmd_queue,

                 laser_moving_flag: Value,
                 laser_finished_flag: Value,
                 start_capture_flag: Value,
                 kill_flag: Value,
                 internal_log, internal_log_level):
        super().__init__(state_queue, cmd_queue,
                         kill_flag=kill_flag,
                         internal_log=internal_log,
                         internal_log_level=internal_log_level,)

        self.logger, self.ha = None, None
        # if not self.logger.handlers:
        #     self.logger.setLevel(level=logging.DEBUG)
        # self.logger.disabled = False
        # print(self.logger)
        # self.logger.info(f"Created logger for {self.__class__.__name__}({os.getpid()})")

        self.laser_moving_flag = laser_moving_flag
        self.laser_finished_flag = laser_finished_flag
        self.start_capture_flag = start_capture_flag

    def init_loggers(self):
        self.logger, self.ha = self.create_new_logger(f"{self.__class__.__name__}/({os.getpid()})")

    def wrap_func(self, func, con: LaserCon = None, usb_port: str = None):
        res = None
        if usb_port is not None and con is None:
            with LaserCon(usb_port) as con:
                self.get_connected(con)
                res = func(con)
            self.get_connected(con)
        elif usb_port is None and con is not None and isinstance(con, LaserCon):
            res = func(con)
        elif usb_port is None and con is None:
            self.logger.error("USB Port or a connection object must be provided!")
            raise ValueError("USB Port or a connection object must be provided!")
        #self.logger.debug(f"Result of {func.__name__} is {res}")
        return res

    @cmp.CProcess.register_signal(postfix="_finished")
    def get_connected(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> bool:
        def func(_con: LaserCon):
            return _con.connected

        return self.wrap_func(func, con, usb_port)

    @cmp.CProcess.register_signal(postfix="_finished")
    def get_current_wavelength(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> float:
        def func(_con: LaserCon):
            return _con.current_wavelength

        return self.wrap_func(func, con, usb_port)

    @cmp.CProcess.register_signal(postfix="_finished")
    def get_min_wavelength(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> float:
        def func(_con: LaserCon):
            return _con.min_wavelength

        return self.wrap_func(func, con, usb_port)

    @cmp.CProcess.register_signal(postfix="_finished")
    def get_max_wavelength(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> float:
        def func(_con: LaserCon):
            return _con.max_wavelength

        return self.wrap_func(func, con, usb_port)

    @cmp.CProcess.register_signal(postfix="_finished")
    def get_velocity(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> float:
        def func(_con: LaserCon):
            return _con.velocity

        return self.wrap_func(func, con, usb_port)

    @cmp.CProcess.register_signal()
    def get_acceleration(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> float:
        def func(con: LaserCon): return con.acceleration

        return self.wrap_func(func, con, usb_port)

    @cmp.CProcess.register_signal(postfix="_finished")
    def get_deceleration(self, con: LaserCon = None, usb_port: str = None, *args, **kwargs) -> float:
        def func(_con: LaserCon):
            return _con.deceleration

        return self.wrap_func(func, con, usb_port)

    def mp_read_laser_settings(self, usb_port: str = None, con: LaserCon = None, *args, **kwargs):
        self.logger.info(f"Reading laser settings from process using {usb_port}")

        def _read(con: LaserCon):
            self.get_connected(con)
            self.get_min_wavelength(con)
            self.get_max_wavelength(con)
            self.get_current_wavelength(con)
            self.get_velocity(con)
            self.get_acceleration(con)
            self.get_deceleration(con)

        self.wrap_func(_read, con, usb_port)

    @cmp.CProcess.register_signal(postfix="_changed")
    def laser_is_moving(self, moving: bool, to_wavelength: float = -1):
        self.laser_moving_flag.value = moving
        return self.laser_moving_flag.value, to_wavelength

    @cmp.CProcess.register_signal(postfix="_changed")
    def movement_finished(self, finished: bool):
        self.laser_finished_flag.value = finished
        return self.laser_finished_flag.value

    @cmp.CProcess.register_signal(postfix="_finished")
    def move_to_wavelength(self, usb_port: str = None, wavelength: float = None, capture: bool = False,
                           con: LaserCon = None, *args, **kwargs):
        # laser_moving_flag.value = False
        def _move(con: LaserCon):
            self.mp_read_laser_settings(usb_port, con)
            self.laser_is_moving(False)
            self.laser_finished_flag.value = False
            # current_wavelength.value = con.current_wavelength
            # laser_connected_flag.value = con.connected
            # log_debug(f"Current Wavelength: {current_wavelength.value}")

            # Move the laser to the new wavelength
            # f = io.StringIO()

            time_start = 0
            # with stdout_redirector(f) as s:
            print(self.logger)
            self._internal_logger.info(f"**** Go to selected wavelength. Started moving laser to {wavelength}. ****")
            # laser_finished_flag.value = False
            # laser_moving_flag.value = True
            # if capture_device_started_flag is not None:
            #    capture_device_started_flag.value = True
            time_start = time.time()
            self.laser_is_moving(True, wavelength)
            if capture:
                self.start_capture_flag.value = int(True)
                self.logger.info(
                    f"******************** Capture flag set to {self.start_capture_flag.value} **********************")
            con.go_to_wvl(wavelength, False)
            self.start_capture_flag.value = int(False)
            self._internal_logger.info(
                f"******************** Capture flag set to {self.start_capture_flag.value} **********************")
            self.laser_is_moving(False)
            time_end = time.time()
            # if capture_device_started_flag is not None:
            #    capture_device_started_flag.value = False
            # laser_finished_flag.value = True
            # laser_moving_flag.value = False
            self.logger.info(f"Go to selected wavelength finished.")

            # current_wavelength.value = con.current_wavelength
            self.logger.info(
                f"Current Wavelength: {self.get_current_wavelength(con)}. Took {time_end - time_start} seconds to move.")
            self.mp_read_laser_settings(usb_port, con)
            # laser_connected_flag.value = False  # We need to manually set this
            return self.get_current_wavelength(con)

        return self.wrap_func(_move, con, usb_port)

    def wavelength_sweep(self, usb_port: str = None,
                         wavelength_start: float = None,
                         wavelength_end: float = None, *args, **kwargs):

        # laser_finished_flag.value = False
        # laser_state.value.connected = False
        self.logger.info(f"Starting sweep from {wavelength_start} to {wavelength_end}.")
        self.logger.info(f"Resetting laser to start wavelength {wavelength_start}")
        self.move_to_wavelength(usb_port, wavelength_start)
        self.logger.info(f"Starting sweep from {wavelength_start} to {wavelength_end}.")
        self.move_to_wavelength(usb_port, wavelength_end, capture=True)
        self.logger.info(f"Finished sweep from {wavelength_start} to {wavelength_end}.")
        # laser_state.connected = False
