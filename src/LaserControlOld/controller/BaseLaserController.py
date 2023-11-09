import logging
from multiprocessing import Process

from PySide6.QtCore import QObject, Signal

from AD2CaptDevice.controller.BaseAD2CaptDevice import BaseAD2CaptDevice
from collections.abc import Callable

from src.LaserControlOld.model.LaserModel import LaserSignals, LaserModel

import time


class LaserNotConnectedError(Exception):
    pass

    def __init__(self, message="Fails to open USB0! Please check if USB is connected."):
        self.message = message
        super().__init__(self.message)


class BaseLaserController(QObject, Process):
    _move_to_wavelength_done_changed = Signal(Callable)

    def __init__(self, laser_model: LaserModel, capt_device):
        super().__init__()
        self.logger = logging.Logger("Laser Driver (Generic)")

        self.model = laser_model

        if capt_device is not None:
            import AD2CaptDevice
            self.capt_device = capt_device

        self.pref = "Laser (Generic)"
        self.port_list = ['Generic']


        self.signals = LaserSignals()

        # Notify when movement is done
        # self._move_to_wavelength_done_changed.connect(self._on_move_to_wavelength_done)

    def read_laser_settings(self):
        raise NotImplementedError()

    # ==================================================================================================================
    # c++ function wrappers
    # ==================================================================================================================
    def _c_get_velocity(self) -> float:
        raise NotImplementedError()

    def _c_get_acceleration(self) -> float:
        raise NotImplementedError()

    def _c_get_deceleration(self) -> float:
        raise NotImplementedError()

    def _c_get_current_wavelength(self) -> float:
        raise NotImplementedError()

   
    # ==================================================================================================================
    #
    # ==================================================================================================================
    def read_laser_settings(self):
        pass

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
       """
        Starts the wavelength sweep
       """
       raise NotImplementedError


    def sweep_and_measure(self, start_wavelength: float = None, stop_wavelength: float = None) -> (list, float):
        """
            Starts the sweep and blocks until the sweep has finished
        """
        self.capt_device.reset_capture()
        self.logger.info("**** Sweep and measure task has started! ****")
        self.start_wavelength_sweep(start_wavelength, stop_wavelength)
        time.sleep(1)
        while self.capt_device.model.capturing_finished == False:
            # self.logger.info(f"awaiting: {self.capt_device.model.capturing_finished}")
            time.sleep(1)
        self.logger.info(f"{self.capt_device.model.capturing_finished}: Sweep and measure task has finished!")
        return self.capt_device.model.recorded_samples, self.capt_device.model.recording_time


    def stop_process(self):
        raise NotImplementedError()


















    # =
    def _sweep_move_to_starting_wavelength(self, start_wavelength: float, vel_type: bool):
        to_wl = lambda: self._sweep_move_to_target_wavelength(self.model.sweep_stop_wavelength, vel_type)
        self._move_to_wavelength(start_wavelength,
                                 vel_type=vel_type,
                                 on_start=None,
                                 on_finished=to_wl)

    def _sweep_move_to_target_wavelength(self, stop_wavelength: float, vel_type: bool):
        # self.model.wavelength_sweep_running = True
        self._move_to_wavelength(stop_wavelength,
                                 vel_type=vel_type,
                                 on_start=self.capt_device.start_capture,
                                 on_finished=self.capt_device.stop_capture)

    def reset_laser_position_to_sweep_start(self):
        if self.model.connected:
            self.logger.info(
                f"[{self.pref} Task] - Resetting the position of the laser to {self.model.sweep_start_wavelength}.")
            self.thread_manager.start(lambda: self._move_to_wavelength())
        else:
            self.logger.error("Laser not connected!")

    def _start_wavelength_sweep(self):
        if self.model.connected:
            # self.model.signals.laser_ready_for_sweep_changed.emit(False)
            self.logger.info(
                f"Starting wavelength sweep {self.model.sweep_start_wavelength} - {self.model.sweep_stop_wavelength}")
            # 1. Reset the laser
            self._move_to_wavelength(self.model.sweep_start_wavelength,
                                     vel_type=False,
                                     on_finished=self._sweep_move_to_target_wavelength)

            # Notify the AD2 device, that the should start with it's setup
            self.model.signals.laser_ready_for_sweep_changed.emit(True)
        else:
            self.logger.error("Laser not connected!")

    ## 4. Check the end position
    # self.read_laser_settings()
    # self.logger.info(f"[{self.pref} Task] - Finished wavelength sweep at {self.laser_model.current_wavelength}")
    # return

    # self._thread_wavelength_sweep()

    def _thread_wavelength_sweep(self):
        """
            Emits a signals.wavelength_sweep_started if the sweep has started!
            Emits a signals.wavelength_sweep_finished if the sweep has stopped!

        """
        if self.model.connected:
            # self.logger.info(f"Laser is at position {self.model.current_wavelength}. ")
            self.model.laser_at_position = False
            self.model.laser_is_moving = True
            self.model.signals.wavelength_sweep_running_changed.emit(True)
            self._c_go_to_wvl(self.model.sweep_stop_wavelength, False)
            self.model.signals.wavelength_sweep_running_changed.emit(False)
            self.model.laser_is_moving = False
            self.model.laser_at_position = True
            # self.logger.info(f"Laser moved to position {self.model.current_wavelength}. ")
            self.model.laser_at_position = True
            self.disconnect()

    def open_laser_uncertainty_file(self):
        pass

    def _move_to_wavelength(self, num_wavelength: float, vel_type: bool,
                            on_start: Callable = None,
                            on_finished: Callable = None):
        """
            Moves the laser to the given wavelength and notifies when the movement is done.
            Calls the function on_finished when the movement is done.
            :param num_wavelength: wavelength to move to
            :param vel_type: velocity type (True for fast mode, False for normal mode)
            :param on_start: function to call when the movement starts
            :param on_finished: function to call when the movement is done
        """

        if not self.model.connected:
            self.logger.warning(f"Laser not connected! Trying to connect on previous selected port {self.model.port}.")
            self.connect_device(self.model.port)

        if self.model.connected:
            self.logger.info(f"Laser is at position {self.model.current_wavelength}. Starting the movement thread.")
            self.model.laser_at_position = False
            self.model.laser_is_moving = True
            # Start the movement back to the start wavelength
            # Propagate the on_finished function to the thread
            #self.worker_process = Process(target=self._c_go_to_wvl,
            #                              args=(self.laserconn, num_wavelength,
            #                                    vel_type))
            #self.worker_process.start()
            #self.thread_manager.start(lambda: self._go_to_wavelength(num_wavelength,
            #                                                         vel_type=vel_type,
            #                                                         on_start=on_start,
            #                                                         on_finished=on_finished))
        else:
            self.logger.error("Laser not connected! Aborting movement.")
            self.model.laser_at_position = False
            self.model.laser_is_moving = False