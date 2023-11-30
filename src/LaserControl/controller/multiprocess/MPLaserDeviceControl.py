from multiprocessing import Value

from PySide6.QtCore import Signal
from cmp.CProcessControl import CProcessControl

from LaserControl.controller.multiprocess.MPLaserDevice import MPLaserDevice


class MPLaserDeviceControl(CProcessControl):
    get_connected_finished = Signal(bool)
    get_current_wavelength_finished = Signal(float)
    get_min_wavelength_finished = Signal(float)
    get_max_wavelength_finished = Signal(float)
    get_velocity_finished = Signal(float)
    get_acceleration_finished = Signal(float)
    get_deceleration_finished = Signal(float)
    mp_read_laser_settings_finished = Signal()

    move_to_wavelength_finished = Signal(float)
    wavelength_sweep_finished = Signal(float)

    laser_is_moving_changed = Signal(bool, float)
    movement_finished_changed = Signal(bool)

    def __init__(self, parent,
                 laser_moving_flag: Value,
                 laser_finished_flag: Value,
                 start_capture_flag: Value,
                 enable_logging=False):
        super().__init__(parent, enable_internal_logging=enable_logging)

        self.register_child_process(MPLaserDevice(self.state_queue, self.cmd_queue,
                                                  laser_moving_flag, laser_finished_flag, start_capture_flag,
                                                  enable_internal_logging=enable_logging))

    def set_start_capture_flag(self, start_capture_flag: Value):
        self._start_capture_flag = start_capture_flag

    @CProcessControl.register_function
    def get_connected(self):
        self._internal_logger.info("Reading current connection state from process.")

    @CProcessControl.register_function()
    def get_current_wavelength(self):
        self._internal_logger.info("Reading current wavelength from process.")

    @CProcessControl.register_function()
    def get_min_wavelength(self):
        self._internal_logger.info("Reading minimum wavelength from process.")

    @CProcessControl.register_function()
    def get_max_wavelength(self):
        self._internal_logger.info("Reading maximum wavelength from process.")

    @CProcessControl.register_function()
    def get_velocity(self):
        self._internal_logger.info("Reading velocity from process.")

    @CProcessControl.register_function()
    def get_acceleration(self):
        self._internal_logger.info("Reading acceleration from process.")

    @CProcessControl.register_function()
    def get_deceleration(self):
        self._internal_logger.info("Reading deceleration from process.")

    @CProcessControl.register_function()
    def mp_read_laser_settings(self, usb_port: str):
        self._internal_logger.info(f"Reading laser settings from process using {usb_port}")

    @CProcessControl.register_function()
    def move_to_wavelength(self, usb_port: str, wavelength: float):
        print(f"Moving laser ({usb_port}) to wavelength {wavelength} from process")

    @CProcessControl.register_function()
    def wavelength_sweep(self, usb_port: str, wavelength_start: float, wavelength_end: float):
        print(f"Sweeping laser ({usb_port}): Wavelength {wavelength_start} - {wavelength_end} from process")
