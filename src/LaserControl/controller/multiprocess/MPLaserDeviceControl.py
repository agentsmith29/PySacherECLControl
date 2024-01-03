import logging
from multiprocessing import Value

from PySide6.QtCore import Signal
from cmp.CProcessControl import CProcessControl

from LaserControl.controller.multiprocess.MPLaserDevice import MPLaserDevice


class MPLaserDeviceControl(CProcessControl):
    get_connected_finished = Signal(bool, name='get_connected_finished')
    get_current_wavelength_finished = Signal(float, name='get_current_wavelength_finished')
    get_min_wavelength_finished = Signal(float, name='get_min_wavelength_finished')
    get_max_wavelength_finished = Signal(float, name='get_max_wavelength_finished')
    get_velocity_finished = Signal(float, name='get_velocity_finished')
    get_acceleration_finished = Signal(float, name='get_acceleration_finished')
    get_deceleration_finished = Signal(float, name='get_deceleration_finished')
    mp_read_laser_settings_finished = Signal(name='mp_read_laser_settings_finished')

    move_to_wavelength_finished = Signal(float, name='move_to_wavelength_finished')
    wavelength_sweep_finished = Signal(float, float, name='wavelength_sweep_finished')

    laser_is_moving_changed = Signal(bool, float, name='laser_is_moving_changed')
    movement_finished_changed = Signal(bool, name='movement_finished_changed')

    def __init__(self, parent,
                 laser_moving_flag: Value,
                 laser_finished_flag: Value,
                 start_capture_flag: Value,
                 enable_logging=False):
        super().__init__(parent, internal_log_level=logging.DEBUG, internal_log=True)

        self.register_child_process(MPLaserDevice,
                                    laser_moving_flag,
                                    laser_finished_flag,
                                    start_capture_flag)

    def set_start_capture_flag(self, start_capture_flag: Value):
        self._start_capture_flag = start_capture_flag

    @CProcessControl.register_function(get_connected_finished)
    def get_connected(self):
        self._internal_logger.info("Reading current connection state from process.")

    @CProcessControl.register_function(get_current_wavelength_finished)
    def get_current_wavelength(self):
        self._internal_logger.info("Reading current wavelength from process.")

    @CProcessControl.register_function(get_min_wavelength_finished)
    def get_min_wavelength(self):
        self._internal_logger.info("Reading minimum wavelength from process.")

    @CProcessControl.register_function(get_max_wavelength_finished)
    def get_max_wavelength(self):
        self._internal_logger.info("Reading maximum wavelength from process.")

    @CProcessControl.register_function(get_velocity_finished)
    def get_velocity(self):
        self._internal_logger.info("Reading velocity from process.")

    @CProcessControl.register_function(get_acceleration_finished)
    def get_acceleration(self):
        self._internal_logger.info("Reading acceleration from process.")

    @CProcessControl.register_function(get_deceleration_finished)
    def get_deceleration(self):
        self._internal_logger.info("Reading deceleration from process.")

    @CProcessControl.register_function(mp_read_laser_settings_finished)
    def mp_read_laser_settings(self, usb_port: str):
        self._internal_logger.info(f"Reading laser settings from process using {usb_port}")

    @CProcessControl.register_function(move_to_wavelength_finished)
    def move_to_wavelength(self, usb_port: str, wavelength: float):
        print(f"Moving laser ({usb_port}) to wavelength {wavelength} from process")

    @CProcessControl.register_function(wavelength_sweep_finished)
    def wavelength_sweep(self, usb_port: str, wavelength_start: float, wavelength_end: float):
        print(f"Sweeping laser ({usb_port}): Wavelength {wavelength_start} - {wavelength_end} from process")
