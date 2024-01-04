import logging
from multiprocessing import Value, Lock

import CaptDeviceControl as captdev
import cmp
from PySide6.QtCore import Signal
from cmp.CProcessControl import CProcessControl

from LaserControl.controller.multiprocess.MPLaserDevice import MPLaserDevice
from LaserControl.model.LaserControlModel import LaserControlModel


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

    def __init__(self, model: LaserControlModel,
                 start_capture_flag: Value,
                 internal_log_level=logging.WARNING,
                 internal_log=True,
                 log_file=None):
        super().__init__(internal_log_level=internal_log_level, internal_log=internal_log, log_file=log_file)

        self.model = model

        self.lock = Lock()
        self._laser_moving_flag = Value('i', False, lock=self.lock)
        self._laser_finished_flag = Value('i', False, lock=self.lock)

        self.register_child_process(MPLaserDevice,
                                    self._laser_moving_flag,
                                    self._laser_finished_flag,
                                    start_capture_flag)


        self.get_connected_finished.connect(
            lambda x: type(self.model).connected.fset(self.model, bool(x)))

        self.get_current_wavelength_finished.connect(
            lambda x: type(self.model).current_wavelength.fset(self.model, x))

        self.get_min_wavelength_finished.connect(
            lambda x: type(self.model).min_laser_wavelength.fset(self.model, x))

        self.get_max_wavelength_finished.connect(
            lambda x: type(self.model).max_laser_wavelength.fset(self.model, x))

        self.get_velocity_finished.connect(
            lambda x: type(self.model).velocity.fset(self.model, x))

        self.get_acceleration_finished.connect(
            lambda x: type(self.model).acceleration.fset(self.model, x))

        self.get_deceleration_finished.connect(
            lambda x: type(self.model).deceleration.fset(self.model, x))

        self.move_to_wavelength_finished.connect(self._move_to_wavelength_finished)

        self.laser_is_moving_changed.connect(self._laser_is_moving_changed)
        self.movement_finished_changed.connect(self._laser_movement_finished)

        self.kill_thread = False

    def set_start_capture_flag(self, start_capture_flag: Value):
        self._start_capture_flag = start_capture_flag

    @cmp.CProcessControl.register_function(get_connected_finished)
    def get_connected(self):
        self._internal_logger.info("Reading current connection state from process.")

    @cmp.CProcessControl.register_function(get_current_wavelength_finished)
    def get_current_wavelength(self):
        self._internal_logger.info("Reading current wavelength from process.")

    @cmp.CProcessControl.register_function(get_min_wavelength_finished)
    def get_min_wavelength(self):
        self._internal_logger.info("Reading minimum wavelength from process.")

    @cmp.CProcessControl.register_function(get_max_wavelength_finished)
    def get_max_wavelength(self):
        self._internal_logger.info("Reading maximum wavelength from process.")

    @CProcessControl.register_function(get_velocity_finished)
    def get_velocity(self):
        self._internal_logger.info("Reading velocity from process.")

    @cmp.CProcessControl.register_function(get_acceleration_finished)
    def get_acceleration(self):
        self._internal_logger.info("Reading acceleration from process.")

    @cmp.CProcessControl.register_function(get_deceleration_finished)
    def get_deceleration(self):
        self._internal_logger.info("Reading deceleration from process.")

    @cmp.CProcessControl.register_function(mp_read_laser_settings_finished)
    def mp_read_laser_settings(self, usb_port: str):
        self._internal_logger.info(f"Reading laser settings from process using {usb_port}")

    @cmp.CProcessControl.register_function(move_to_wavelength_finished)
    def move_to_wavelength(self, usb_port: str, wavelength: float):
        print(f"Moving laser ({usb_port}) to wavelength {wavelength} from process")

    @cmp.CProcessControl.register_function(wavelength_sweep_finished)
    def wavelength_sweep(self, usb_port: str, wavelength_start: float, wavelength_end: float):
        print(f"Sweeping laser ({usb_port}): Wavelength {wavelength_start} - {wavelength_end} from process")

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def connect_capture_device(self, device: captdev.Controller):
        self.logger.info(
            "***********************************************Connecting to capture device..***********************************")
        self.mp_read_laser_settings(self.model.port)
        if isinstance(device, captdev.Controller):
            self.model.capturing_device = device
            self.model.capturing_device.model.device_information.signals.device_connected_changed.connect(
                lambda x: type(self.model).capturing_device_connected.fset(self.model, x)
            )

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

    def start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
        # self.capt_device.clear_data()
        # Reset the flag
        # self.capt_device.model.capturing_finished = False
        self.logger.info(f"Starting wavelength sweep from {start_wavelength} to {stop_wavelength}")
        if self.model.capturing_device is not None:
            self.model.capturing_device.reset_capture()
            if not self.model.capturing_device.model.device_information.device_connected:
                #self.model.
                self.model.capturing_device.open_device()
                self.model.capturing_device.ready_for_recording_changed.connect(
                    lambda ready: self.start_wavelength_sweep_emitted(start_wavelength, stop_wavelength, ready=ready)
                )
            self.logger.info("Capturing device is connected.")

            if self.model.capturing_device.model.capturing_information.ready_for_recording:
                self.start_wavelength_sweep_emitted(start_wavelength, stop_wavelength)
        else:
            self.start_wavelength_sweep_emitted(start_wavelength, stop_wavelength)

    def start_wavelength_sweep_emitted(self, start_wavelength: float = None, stop_wavelength: float = None, ready=True):
        if ready:
            if start_wavelength is None:
                start_wavelength = self.model.sweep_start_wavelength
            if stop_wavelength is None:
                stop_wavelength = self.model.sweep_stop_wavelength
            self.wavelength_sweep(self.model.port, start_wavelength, stop_wavelength)