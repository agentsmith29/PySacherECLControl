import logging
import time
from multiprocessing import Value, Lock, Process

from PySide6.QtCore import QThreadPool

from model.LaserControlModel import LaserControlModel
from controller.LaserCon import LaserCon
from controller.multiprocess.LaserStateArray import LaserStateArray
from controller.multiprocess.move_to_wavelength import move_to_wavelength
from controller.multiprocess.wavelength_sweep import wavelength_sweep


class LaserControlController:

    def __init__(self, model: LaserControlModel):

        self.logger = logging.Logger("Laser Driver (Generic)")

        self.model = model

        # Multiprocess variables
        self.proc: Process = None
        self.lock = Lock()
        self._laser_port = Value('i', 0, lock=self.lock)
        self._laser_connected_flag = Value('i', False, lock=self.lock)
        self._laser_moving_flag = Value('i', False, lock=self.lock)
        self._laser_finished_flag = Value('i', False, lock=self.lock)
        self._current_wavelength = Value('f', 0.0, lock=self.lock)

        self._laser_state = Value(LaserStateArray, (False, False, False, 0, 0, 0), lock=self.lock)

        # For the sweep
        self.laser_at_start_position_flag = Value('i', False, lock=self.lock)
        self.laser_at_end_position_flag = Value('i', False, lock=self.lock)

        # Threads for acquiring data from the process
        self.thread_manager = QThreadPool()
        self.kill_thread = False
        self.thread_manager.start(self._monitor_laser_state)

    def connect_device(self):
        self.logger.info("Connecting to laser...")


    def _monitor_laser_state(self):
        while not self.kill_thread:
            self.model.connected = bool(self._laser_connected_flag.value)
            self.model.laser_is_moving = bool(self._laser_moving_flag.value)
            self.model.laser_at_position = bool(self._laser_finished_flag.value)
            self.model.current_wavelength = float(self._current_wavelength.value)
            #print(self._laser_state.connected)
            #print("Monitor")
            time.sleep(0.1)
        self.logger.info("Monitor Laser State Thread Ended")
        # Reset the flag
        self._laser_finished_flag.value = False

    def read_laser_settings(self):
        self.logger.info("Reading laser settings...")
        with LaserCon() as con:
            self.model.connected = con.connected
            self.model.min_laser_wavelength = con.min_wavelength
            self.model.max_laser_wavelength = con.max_wavelength
            self.model.current_wavelength = con.current_wavelength
            self.model.velocity = con.velocity
            self.model.acceleration = con.acceleration


        self.model.connected = False

    def start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
        # self.capt_device.clear_data()
        # Reset the flag
        # self.capt_device.model.capturing_finished = False

        if start_wavelength is None:
            start_wavelength = self.model.sweep_start_wavelength
        if stop_wavelength is None:
            stop_wavelength = self.model.sweep_stop_wavelength

        self.proc = Process(target=wavelength_sweep,
                            args=(self._laser_port,
                                  self._current_wavelength,
                                  self._laser_connected_flag,
                                  self._laser_moving_flag,
                                  self.laser_at_start_position_flag,
                                  self.laser_at_end_position_flag,
                                  # self.capt_device.start_capture_flag,
                                  self.laser_at_end_position_flag,
                                  self._laser_finished_flag,
                                  start_wavelength, stop_wavelength,
                                  self._laser_state))
        self.proc.start()
        self.logger.info("Sweep Process Started")
        # self.thread_manager.start(self._monitor_laser_state)

    def move_to_wavelength(self, wavelength: float) -> None:
        self.proc = Process(target=move_to_wavelength,
                            args=(self._laser_port, self._current_wavelength,
                                  self._laser_connected_flag,
                                  self._laser_moving_flag,
                                  self._laser_finished_flag,
                                  wavelength))
        self.proc.start()
        self.logger.info("Move to Wavelength Process Started")
        # self.thread_manager.start(self._monitor_laser_state)

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
