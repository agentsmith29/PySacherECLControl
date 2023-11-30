import logging
import time
from multiprocessing import Value, Lock, Process

from PySide6.QtCore import QThreadPool

from LaserControl.controller.multiprocess.MPLaserDeviceControl import MPLaserDeviceControl
from LaserControl.model.LaserControlModel import LaserControlModel

import CaptDeviceControl as captdev

class LaserControlController:

    def __init__(self, model: LaserControlModel, start_capture_flag: Value):

        self.logger = logging.Logger("Laser Driver (Generic)")

        self.model = model

        # Multiprocess variables
        #self.proc: Process = None
        self.lock = Lock()
        #self._laser_port = Value('i', 0, lock=self.lock)
        #self._laser_connected_flag = Value('i', False, lock=self.lock)

        self._laser_moving_flag = Value('i', False, lock=self.lock)
        self._laser_finished_flag = Value('i', False, lock=self.lock)

        #if self.model.capturing_device is None or not self.model.capturing_device_connected:
        self._start_capture_flag = start_capture_flag
        #else:
        #    self._start_capture_flag = self.model.capturing_device.start_capture_flag

        #self._current_wavelength = Value('f', 0.0, lock=self.lock)

        #self._laser_state = Value(LaserStateArray, (False, False, False, 0, 0, 0), lock=self.lock)

        # For the sweep
        #self.laser_at_start_position_flag = Value('i', False, lock=self.lock)
        #self.laser_at_end_position_flag = Value('i', False, lock=self.lock)

        # Threads for acquiring data from the process
        #self.thread_manager = QThreadPool()
        self.mp_laser_controller = MPLaserDeviceControl(None,
                                                        self._laser_moving_flag,
                                                        self._laser_finished_flag,
                                                        self._start_capture_flag,
                                                        enable_logging=False)

        self.mp_laser_controller.get_connected_finished.connect(
            lambda x: type(self.model).connected.fset(self.model, bool(x)))

        self.mp_laser_controller.get_current_wavelength_finished.connect(
            lambda x: type(self.model).current_wavelength.fset(self.model, x))

        self.mp_laser_controller.get_min_wavelength_finished.connect(
            lambda x: type(self.model).min_laser_wavelength.fset(self.model, x))

        self.mp_laser_controller.get_max_wavelength_finished.connect(
            lambda x: type(self.model).max_laser_wavelength.fset(self.model, x))

        self.mp_laser_controller.get_velocity_finished.connect(
            lambda x: type(self.model).velocity.fset(self.model, x))

        self.mp_laser_controller.get_acceleration_finished.connect(
            lambda x: type(self.model).acceleration.fset(self.model, x))

        self.mp_laser_controller.get_deceleration_finished.connect(
            lambda x: type(self.model).deceleration.fset(self.model, x))

        self.mp_laser_controller.move_to_wavelength_finished.connect(self._move_to_wavelength_finished)

        self.mp_laser_controller.laser_is_moving_changed.connect(self._laser_is_moving_changed)
        self.mp_laser_controller.movement_finished_changed.connect(self._laser_movement_finished)

        self.kill_thread = False


    def connect_capture_device(self, device: captdev.Controller):
        self.logger.info("***********************************************Connecting to capture device..***********************************")
        self.mp_laser_controller.mp_read_laser_settings(self.model.port)
        if isinstance(device, captdev.Controller):
            self.model.capturing_device = device
            self.model.capturing_device_connected = True



    def connect_device(self):
        self.logger.info("Connecting to laser...")
        self.mp_laser_controller.mp_read_laser_settings(self.model.port)


    def _move_to_wavelength_finished(self, wavelength: float):
        self.logger.info(f"Move to wavelength finished. Current wavelength: {wavelength}")

    def _laser_is_moving_changed(self, is_moving: bool, to_wavelength: float):
        self.logger.info(f"************** Laser is moving: {is_moving}."
                         f"Moving to {self.model.laser_moving_to_wavelength} nm")
        self.model.laser_is_moving = (is_moving, to_wavelength)
        self.logger.info(f"************** Laser is moving: {is_moving}."
                         f"Moving to {self.model.laser_moving_to_wavelength} nm")

    def _laser_movement_finished(self, is_finished: bool):
        pass


    # def _monitor_laser_state(self):
    #     while not self.kill_thread:
    #         self.model.connected = bool(self._laser_connected_flag.value)
    #         self.model.laser_is_moving = bool(self._laser_moving_flag.value)
    #         self.model.laser_at_position = bool(self._laser_finished_flag.value)
    #         self.model.current_wavelength = float(self._current_wavelength.value)
    #         #print(self._laser_state.connected)
    #         #print("Monitor")
    #         time.sleep(0.1)
    #     self.logger.info("Monitor Laser State Thread Ended")
    #     # Reset the flag
    #     self._laser_finished_flag.value = False

    # def read_laser_settings(self):
    #     self.logger.info("Reading laser settings...")
    #     with LaserCon() as con:
    #         self.model.connected = con.connected
    #         self.model.min_laser_wavelength = con.min_wavelength
    #         self.model.max_laser_wavelength = con.max_wavelength
    #         self.model.current_wavelength = con.current_wavelength
    #         self.model.velocity = con.velocity
    #         self.model.acceleration = con.acceleration
    #
    #
    #     self.model.connected = False

    def start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
        # self.capt_device.clear_data()
        # Reset the flag
        # self.capt_device.model.capturing_finished = False

        if start_wavelength is None:
            start_wavelength = self.model.sweep_start_wavelength
        if stop_wavelength is None:
            stop_wavelength = self.model.sweep_stop_wavelength
        self.mp_laser_controller.wavelength_sweep(self.model.port, start_wavelength, stop_wavelength)

    def move_to_wavelength(self, wavelength: float) -> None:
        self.logger.info(f"Move to wavelength {wavelength}")
        self.mp_laser_controller.move_to_wavelength(self.model.port, wavelength)

    def stop_process(self):
        time_start = time.time()
        if self.proc is not None:
            while self.proc.is_alive():
                time.sleep(0.1)
            self.logger.warning(f"Laser process exited after {time.time() - time_start}s")
        self.kill_thread = True

    def __del__(self):
        self.logger.info("Exiting Laser controller")
        self.stop_process()
        self.logger.warning("Laser controller exited")
