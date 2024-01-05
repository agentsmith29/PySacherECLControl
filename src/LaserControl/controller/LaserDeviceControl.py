import logging
from multiprocessing import Value, Lock

import CaptDeviceControl as captdev
import cmp
from PySide6.QtCore import Signal
from cmp.CProcessControl import CProcessControl

from LaserControl.controller.multiprocess.MPLaserDevice import MPLaserDevice
from LaserControl.model.LaserControlModel import LaserControlModel


class MPLaserDeviceControl(CProcessControl):
    connected_changed = Signal(bool, name='connected_changed')
    current_wavelength_changed = Signal(float, name='current_wavelength_changed')


    get_min_wavelength_finished = Signal(float, name='get_min_wavelength_finished')
    get_max_wavelength_finished = Signal(float, name='get_max_wavelength_finished')
    get_velocity_finished = Signal(float, name='get_velocity_finished')
    get_acceleration_finished = Signal(float, name='get_acceleration_finished')
    get_deceleration_finished = Signal(float, name='get_deceleration_finished')
    mp_read_laser_settings_finished = Signal(name='mp_read_laser_settings_finished')

    move_to_wavelength_finished = Signal(float, name='move_to_wavelength_finished')
    wavelength_sweep_finished = Signal(float, float, name='wavelength_sweep_finished')

    laser_is_moving_changed = Signal(bool, float, name='laser_is_moving_changed')
    wavelength_sweep_running_changed = Signal(bool, name='wavelength_sweep_running_changed')
    movement_finished_changed = Signal(bool, name='movement_finished_changed')

    def __init__(self, model: LaserControlModel,
                 start_capture_flag: Value):
        super().__init__()

        self.model = model

        self.lock = Lock()
        self._laser_moving_flag = Value('i', False, lock=self.lock)
        self._laser_finished_flag = Value('i', False, lock=self.lock)
        if start_capture_flag is None:
            start_capture_flag = Value('i', 0)

        self.register_child_process(MPLaserDevice,
                                    self._laser_moving_flag,
                                    self._laser_finished_flag,
                                    start_capture_flag)

        self.connected_changed.connect(
            lambda x: type(self.model).connected.fset(self.model, bool(x)))

        self.current_wavelength_changed.connect(
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
        self.wavelength_sweep_running_changed.connect(self._on_wavelength_sweep_running_changed)

        self.kill_thread = False

    def set_start_capture_flag(self, start_capture_flag: Value):
        self._start_capture_flag = start_capture_flag

    @cmp.CProcessControl.register_function(connected_changed)
    def get_connected(self):
        self._module_logger.info("Reading current connection state from process.")

    @cmp.CProcessControl.register_function(current_wavelength_changed)
    def get_current_wavelength(self):
        self._module_logger.info("Reading current wavelength from process.")

    @cmp.CProcessControl.register_function(get_min_wavelength_finished)
    def get_min_wavelength(self):
        self._module_logger.info("Reading minimum wavelength from process.")

    @cmp.CProcessControl.register_function(get_max_wavelength_finished)
    def get_max_wavelength(self):
        self._module_logger.info("Reading maximum wavelength from process.")

    @CProcessControl.register_function(get_velocity_finished)
    def get_velocity(self):
        self._module_logger.info("Reading velocity from process.")

    @cmp.CProcessControl.register_function(get_acceleration_finished)
    def get_acceleration(self):
        self._module_logger.info("Reading acceleration from process.")

    @cmp.CProcessControl.register_function(get_deceleration_finished)
    def get_deceleration(self):
        self._module_logger.info("Reading deceleration from process.")

    @cmp.CProcessControl.register_function(mp_read_laser_settings_finished)
    def read_laser_settings(self, usb_port: str):
        self._module_logger.info(f"Reading laser settings from process using {usb_port}")

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
        self.read_laser_settings(self.model.port)
        if isinstance(device, captdev.Controller):
            self.model.capturing_device = device
            self.model.capturing_device.model.device_information.signals.device_connected_changed.connect(
                lambda x: type(self.model).capturing_device_connected.fset(self.model, x)
            )

    def _move_to_wavelength_finished(self, wavelength: float):
        self.logger.info(f"Move to wavelength finished. Current wavelength: {wavelength}")

    def _laser_is_moving_changed(self, is_moving: bool, to_wavelength: float):
        self.logger.info(f"************** Laser is moving: {is_moving}. "
                         f"Moving to {self.model.laser_moving_to_wavelength} nm")
        self.model.laser_is_moving = (is_moving, to_wavelength)
        self.logger.info(f"************** Laser is moving: {is_moving}. "
                         f"Moving to {self.model.laser_moving_to_wavelength} nm")

    def _laser_movement_finished(self, is_finished: bool):
        pass

    def _on_wavelength_sweep_running_changed(self, running: bool):
        self.model.wavelength_sweep_running = running
        if running:
            self.logger.info(f"Wavelength sweep running.")
        else:
            self.logger.info(f"Wavelength sweep stopped.")

    def start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
        self.model.wavelength_sweep_running = True
        self.logger.info(f"Starting wavelength sweep from {start_wavelength} to {stop_wavelength}")
        if self.model.capturing_device is not None:
            self.model.capturing_device.reset_capture()
            if not self.model.capturing_device.model.device_information.device_connected:
                # self.model.
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
