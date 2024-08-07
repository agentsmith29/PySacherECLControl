import logging
from multiprocessing import Value, Lock

import ADScopeControl as captdev
import mpPy6
from PySide6.QtCore import Signal
from mpPy6.CProcessControl import CProcessControl

from SacherECLControl.controller.multiprocess.MPLaserDevice import MPLaserDevice
from SacherECLControl.model.LaserControlModel import LaserControlModel


class MPLaserDeviceControl(CProcessControl):
    connected_changed = Signal(bool, name='connected_changed')

    # Properties, automatically triggerd on a change by the process class
    current_wavelength_changed = Signal(float, name='current_wavelength_changed')
    min_wavelength_changed = Signal(float, name='min_wavelength_changed')
    max_wavelength_changed = Signal(float, name='max_wavelength_changed')
    velocity_changed = Signal(float, name='velocity_changed')
    acceleration_changed = Signal(float, name='acceleration_changed')
    deceleration_changed = Signal(float, name='deceleration_changed')

    ## Triggered when the laser settings are changed
    laser_settings_changed = Signal(float, name='laser_settings_changed')




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

    start_wavelength_sweep = Signal(float, float, name='start_wavelength_sweep')

    def __init__(self, model: LaserControlModel,
                 start_capture_flag: Value, module_log=True, module_log_level=logging.WARNING):
        super().__init__(module_log=module_log, module_log_level=module_log_level)

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

        self.connected_changed.connect(self._on_connected_changed)

        self.current_wavelength_changed.connect(
            lambda x: type(self.model).current_wavelength.fset(self.model, x))

        self.min_wavelength_changed.connect(
            lambda x: type(self.model).min_laser_wavelength.fset(self.model, x))

        self.max_wavelength_changed.connect(
            lambda x: type(self.model).max_laser_wavelength.fset(self.model, x))

        self.velocity_changed.connect(
            lambda x: type(self.model).velocity.fset(self.model, x))

        self.acceleration_changed.connect(
            lambda x: type(self.model).acceleration.fset(self.model, x))

        self.deceleration_changed.connect(
            lambda x: type(self.model).deceleration.fset(self.model, x))

        self.move_to_wavelength_finished.connect(self._move_to_wavelength_finished)

        self.laser_is_moving_changed.connect(self._laser_is_moving_changed)
        self.movement_finished_changed.connect(self._laser_movement_finished)
        self.wavelength_sweep_running_changed.connect(self._on_wavelength_sweep_running_changed)

        self.start_wavelength_sweep.connect(self._start_wavelength_sweep)
        self.kill_thread = False

    def _on_connected_changed(self, connected: bool):
        if connected:
            self.logger.info(f"[{connected}] Laser connection established.")
        else:
            self.logger.info(f"[{connected}] Laser disconnected.")
        self.model.connected = connected

    # ==================================================================================================================
    # Connection
    # ==================================================================================================================
    @mpPy6.CProcessControl.register_function()
    def connect_device(self, usb_port: str):
        """
        Establishes a connection to the Epos and reads all the needed data saved on the internal registry.
        :param usb_port: usb port on which the connection should be established.
        """
        self._module_logger.info(f"Connecting to process using {usb_port}")

    @mpPy6.CProcessControl.register_function()
    def disconnect_device(self):
        """
        Disconnects the Epos device/laser.
        """
        self._module_logger.info("Disconnecting from laser.")

    @mpPy6.CProcessControl.register_function()
    def set_velocity(self, velocity: float) -> None:
        """ Set the velocity of the laser. """
        self._module_logger.info(f"Setting velocity to {velocity}.")

    @mpPy6.CProcessControl.register_function()
    def set_acceleration(self, acceleration: float) -> None:
        """ Set the velocity of the laser. """
        self._module_logger.info(f"Setting acceleration to {acceleration}.")

    @mpPy6.CProcessControl.register_function()
    def set_deceleration(self, acceleration: float) -> None:
        """ Set the velocity of the laser. """
        self._module_logger.info(f"Setting acceleration to {acceleration}.")

    def set_start_capture_flag(self, start_capture_flag: Value):
        self._start_capture_flag = start_capture_flag

    @mpPy6.CProcessControl.register_function(connected_changed)
    def get_connected(self):
        self._module_logger.info("Reading current connection state from process.")

    @mpPy6.CProcessControl.register_function(laser_settings_changed)
    def get_laser_settings(self):
        self._module_logger.info("Reading current laser status.")

    @mpPy6.CProcessControl.register_function(move_to_wavelength_finished)
    def move_to_wavelength(self, usb_port: str, wavelength: float):
        self._module_logger.info(f"Moving laser ({usb_port}) to wavelength {wavelength} from process")

    @mpPy6.CProcessControl.register_function(wavelength_sweep_finished)
    def wavelength_sweep(self, usb_port: str, wavelength_start: float, wavelength_end: float):
        print(f"Sweeping laser ({usb_port}): Wavelength {wavelength_start} - {wavelength_end} from process")

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def connect_capture_device(self, device: captdev.Controller):
        self.logger.info(
            "***********************************************Connecting to capture device..***********************************")
        if isinstance(device, captdev.Controller):
            self.model.capturing_device = device
            self.model.capturing_device.model.device_information.signals.device_connected_changed.connect(
                lambda x: type(self.model).capturing_device_connected.fset(self.model, x)
            )

    def _move_to_wavelength_finished(self, wavelength: float):
        self.logger.info(f"Move to wavelength finished. Current wavelength: {wavelength}")

    def _laser_is_moving_changed(self, is_moving: bool, to_wavelength: float):
        self.model.laser_is_moving = (is_moving, to_wavelength)
        if is_moving:
            self.logger.info(f"************** Laser is moving: {is_moving}. "
                             f"Moving to {self.model.laser_moving_to_wavelength} nm")
        else:
            if is_moving:
                self.logger.info(f"************** Laser is moving: {is_moving}. "
                                 f"Stopped at {self.model.laser_moving_to_wavelength} nm")

    def _laser_movement_finished(self, is_finished: bool):
        pass

    def _on_wavelength_sweep_running_changed(self, running: bool):
        self.model.wavelength_sweep_running = running
        if running:
            self.logger.info(f"Wavelength sweep running.")
        else:
            self.logger.info(f"Wavelength sweep stopped.")

    def _start_wavelength_sweep(self, start_wavelength: float = None, stop_wavelength: float = None) -> None:
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
