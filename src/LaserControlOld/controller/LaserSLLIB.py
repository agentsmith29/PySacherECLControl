import logging
import os
import sys
import io
import tempfile
from contextlib import contextmanager
from multiprocessing import Value, Lock, Queue, Process

from libs.LaserLib import *


from Laser.LaserControl.controller.BaseLaserController import BaseLaserController, LaserNotConnectedError

from PySide6.QtCore import QObject, Slot, QThreadPool, Signal

import ConfigHandler as Config
import time

from Laser.LaserControl.controller.mp_laserController.MPLaserControl import mp_move_to_wavelength, LaserConnection, \
    mp_wavelength_sweep
from Laser.LaserControl.model.LaserModel import LaserModel


class LLIBErrorConvert:

    @staticmethod
    def convert(msg, additional_message=""):

        msg = msg.replace('>>>>>>>>>>>>>>>>>>>>  ', '').strip()

        if "Fails to open" in msg and "Please check if USB is connected" in msg:
            if additional_message is not None or additional_message != "":
                raise LaserNotConnectedError(f"{msg}. {additional_message}")
            else:
                raise LaserNotConnectedError(f"{msg}")
        else:
            return msg


class LaserSLLIB(BaseLaserController):

    def __init__(self, laser_model: LaserModel, capt_device: any = None):
        super().__init__(laser_model, capt_device)
        self.logger = logging.getLogger("Laser Driver (SLLIB)")


        self.laserconn = laserSacher()

        self.port_list = ['USB0', 'USB1', 'USB2', 'USB3', 'USB4', 'USB5', 'USB6', 'USB7', 'USB8', 'USB9']

        self.model.connected = False
        self.signals.connected_changed.connect(self.read_laser_settings)

        self.thread_manager = QThreadPool()
        self.kill_thread = False 

        self.proc = None
        self.lock = Lock()
        self._laser_state_queue = Queue()

        self._laser_port = Value('i', 0, lock=self.lock)
        self._laser_connected_flag = Value('i', False, lock=self.lock)
        self._laser_moving_flag = Value('i', False, lock=self.lock)
        self._laser_finished_flag = Value('i', False, lock=self.lock)
        self._current_wavelength = Value('f', 0.0, lock=self.lock)

        # For the sweep
        self.laser_at_start_position_flag = Value('i', False, lock=self.lock)
        self.laser_at_end_position_flag = Value('i', False, lock=self.lock)

        
        self.read_laser_settings()
        #

        self.logger.debug("Laser Driver (SLLIB) initialized.")


    def _move_to_wavelength(self, wavelength: float, vel_type: bool) -> None:

        self.proc = Process(target=mp_move_to_wavelength,
                            args=(self._laser_port, self._current_wavelength,
                                  self._laser_connected_flag,
                                  self._laser_moving_flag,
                                  self._laser_finished_flag,
                                  wavelength))
        self.proc.start()
        self.logger.info("Move to Wavelength Process Started")
        self.thread_manager.start(self._monitor_laser_state)

        # Start the thread to monitor the laser state

    def start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
        self.capt_device.clear_data()
        # Reset the flag
        self.capt_device.model.capturing_finished = False

        if start_wavelength is None:
            start_wavelength = self.model.sweep_start_wavelength
        if stop_wavelength is None:
           stop_wavelength = self.model.sweep_stop_wavelength

        self.proc = Process(target=mp_wavelength_sweep,
                            args=(self._laser_port,
                                  self._current_wavelength,
                                  self._laser_connected_flag,
                                  self._laser_moving_flag,
                                  self.laser_at_start_position_flag,
                                  self.laser_at_end_position_flag,
                                  self.capt_device.start_capture_flag,
                                  self._laser_finished_flag,
                                  start_wavelength, stop_wavelength))
        self.proc.start()
        self.logger.info("Sweep Process Started")
        self.thread_manager.start(self._monitor_laser_state)

           

    def _monitor_laser_state(self):
        while bool(self._laser_finished_flag.value) is False and not self.kill_thread:
            self.model.connected = bool(self._laser_connected_flag.value)
            self.model.laser_is_moving = bool(self._laser_moving_flag.value)
            self.model.laser_at_position = bool(self._laser_finished_flag.value)
            self.model.current_wavelength = float(self._current_wavelength.value)
            time.sleep(0.1)
        self.logger.info("Monitor Laser State Thread Ended")
        # Reset the flag
        self._laser_finished_flag.value = False


    def read_laser_settings(self):
        with LaserConnection() as lasercon:
            self.model.current_wavelength = lasercon.current_wavelength
            self.model.velocity = lasercon.velocity
            self.model.acceleration = lasercon.acceleration
            self.model.deceleration = lasercon.deceleration
            self.model.min_laser_wavelength = lasercon.min_wavelength
            self.model.max_laser_wavelength = lasercon.max_wavelength

    

    def _set_velocity(self, velocity: float) -> float:
        ''' Wrapper for the C Function call '''
        f = io.StringIO()
        with self.stdout_redirector(f):
            self.laserconn.setVelocity(velocity)
        return self._c_get_velocity()


    def _set_acceleration(self, acceleration) -> float:
        ''' Wrapper for the C Function call '''
        f = io.StringIO()
        with self.stdout_redirector(f):
            self.laserconn.setAcceleration(acceleration)
        return self._c_get_acceleration()


    def _set_deceleration(self, deceleration: float) -> float:
        ''' Wrapper for the C Function call '''
        f = io.StringIO()
        with self.stdout_redirector(f):
            self._set_deceleration(deceleration)
        return self._c_get_deceleration()

    def _c_get_current_wavelength(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laserconn.getCurrentWavelength())

    def _c_get_laser_min_wavelength(self) -> float:
        # TODO: Change the hardcoded values to the actual values
        return float(830)

    def _c_get_laser_max_wavelength(self) -> float:
        # TODO: Change the hardcoded values to the actual values
        return float(870)

    def get_sweep_start_wavelength(self) -> float:
        ''' Wrapper for the C Function call '''
        return self._c_get_laser_min_wavelength()

    def get_sweep_stop_wavelength(self) -> float:
        ''' Wrapper for the C Function call '''
        return self._c_get_laser_min_wavelength()



    def open_laser_uncertainty_file(self):
        pass

    def set_laser_settings(self, velocity, acceleration, deceleration):
        pass

    @contextmanager
    def stdout_redirector(self, stream):
        # The original fd stdout points to. Usually 1 on POSIX systems.
        original_stdout_fd = sys.stdout.fileno()

        def _redirect_stdout(to_fd):
            """Redirect stdout to the given file descriptor."""
            # Flush the C-level buffer stdout
            sys.stdout.flush()
            # libc.fflush(c_stdout)
            # Flush and close sys.stdout - also closes the file descriptor (fd)
            sys.stdout.close()
            # Make original_stdout_fd point to the same file as to_fd
            os.dup2(to_fd, original_stdout_fd)
            # Create a new sys.stdout that points to the redirected fd
            sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

        # Save a copy of the original stdout fd in saved_stdout_fd
        saved_stdout_fd = os.dup(original_stdout_fd)
        try:
            # Create a temporary file and redirect stdout to it
            tfile = tempfile.TemporaryFile(mode='w+b')
            _redirect_stdout(tfile.fileno())
            # Yield to caller, then redirect stdout back to the saved fd
            yield
            _redirect_stdout(saved_stdout_fd)
            # Copy contents of temporary file to the given stream
            tfile.flush()
            tfile.seek(0, io.SEEK_SET)
            redir = tfile.read().decode("utf-8")
            redirtext_stripped = LLIBErrorConvert.convert(redir)
            stream.write(redirtext_stripped)
        finally:
            tfile.close()
            os.close(saved_stdout_fd)
            # os.dup2(saved_stdout_fd, sys.stdout.fileno())
            # sys.stdout = original


    def stop_process(self):
        time_start = time.time()
        if self.proc is not None:
            while self.proc.is_alive():
                time.sleep(0.1)
            self.logger.warning(f"Laser process exited after {time.time()-time_start}s")
        self.kill_thread = True    
        
    def __del__(self):
        self.logger.info("Exiting Laser controller")
        self.stop_process()
        self.logger.warning("Laser controller exited")

    def __del__(self):
        self.disconnect()


if __name__ == "__main__":
    logging.warning("Laser_SLLIB.py is not meant to be run as a script.")
    laser = LaserSLLIB()
