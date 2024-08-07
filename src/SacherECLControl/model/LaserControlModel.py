# import mcpy
import ADScopeControl as captdev

from SacherECLControl.LaserConfig import LaserConfig
from SacherECLControl.model.LaserControlSignals import LaserControlSignals


# from SacherECLControl.model.LaserControlSignals import LaserControllerSignals
# from LaserControlOld.LaserConfig import LaserConfig


class LaserControlModel(object):

    def __init__(self, laser_config: LaserConfig):

        self.signals = LaserControlSignals()
        self._laser_config: LaserConfig = laser_config

        self._connected = False
        self._port = None

        self._laser_connected = False
        self._laser_at_position = False
        self._laser_is_moving = False
        self._wavelength_sweep_running = False
        self._laser_ready_for_sweep = False
        # A class which can be used to export the laser Settings

        self._laser_moving_to_wavelength: float = 0
        self._current_wavelength = -1
        self._min_laser_wavelength = 1
        self._max_laser_wavelength = 99999

        self._min_deceleration = -10
        self._max_deceleration = 10

        self._min_acceleration = -10
        self._max_acceleration = 10

        self._min_velocity = -10
        self._max_velocity = 10

        # Capturing device settings
        self._capturing_device_connected: bool = False
        self._capturing_device: captdev.Controller = None


    @property
    def laser_config(self) -> LaserConfig:
        return self._laser_config

    @laser_config.setter
    def laser_config(self, value: LaserConfig):
        self._laser_config = value
        # self.signals.laser_config_changed.emit(self.laser_properties)

    # @property
    # def laser_properties(self) -> LaserProperties:
    #    return LaserProperties(
    #            mcpy.Rectangular(self.acceleration, 0.01, unit='nm/s', k=2),
    #            mcpy.Rectangular(self.deceleration, 0.01, unit='nm/s', k=2),
    #            mcpy.Rectangular(self.velocity, 0.01, unit='nm/s^2', k=2),
    #            (mcpy.Rectangular(self.sweep_start_wavelength, 0.01, unit='nm', k=2), mcpy.Rectangular(self.sweep_stop_wavelength, 0.01, unit='nm', k=2))
    #        )

    @property
    def laser_ready_for_sweep(self):
        return self._laser_ready_for_sweep

    @laser_ready_for_sweep.setter
    def laser_ready_for_sweep(self, value):
        self._laser_ready_for_sweep = value
        self.signals.laser_ready_for_sweep_changed.emit(self._laser_ready_for_sweep)

    @property
    def laser_at_position(self):
        return self._laser_at_position

    @laser_at_position.setter
    def laser_at_position(self, value):
        self._laser_at_position = value
        self.signals.laser_at_position_changed.emit(self.laser_at_position)

    @property
    def sweep_start_wavelength(self):
        return self.laser_config.wl_sweep_start.get()

    @sweep_start_wavelength.setter
    def sweep_start_wavelength(self, value):
        #if value < self.min_laser_wavelength:
        #    raise Exception(f"Sweep start wavelength ({value}) can not be smaller than "
        #                    f"minimum laser wavelength {self.min_laser_wavelength})!")
        #if value >= self.max_laser_wavelength:
        #    raise Exception(f"Sweep start wavelength ({value}) can not be greater or equal to the "
        #                    f"maximum laser wavelength ({self.min_laser_wavelength})!")
        #if value > self.sweep_stop_wavelength:
        #    raise Exception(f"Sweep start wavelength ({value}) can not be greater than "
        #                    f"sweep stop wavelength ({self.sweep_stop_wavelength})!")
        self.laser_config.wl_sweep_start.set(value)
        self.signals.sweep_start_wavelength_changed.emit(self.sweep_start_wavelength)

    @property
    def sweep_stop_wavelength(self) -> float:
        return self.laser_config.wl_sweep_stop.get()

    @sweep_stop_wavelength.setter
    def sweep_stop_wavelength(self, value):
        #if value < self.min_laser_wavelength:
        #    raise Exception(f"Sweep stop wavelength ({value}) can not be smaller than "
        #                    f"minimum laser wavelength {self.min_laser_wavelength})!")
        #if value > self.max_laser_wavelength:
        #    raise Exception(f"Sweep stop wavelength ({value}) can not be greater or equal to the "
        #                    f"maximum laser wavelength ({self.max_laser_wavelength})!")
        #if value < self.sweep_start_wavelength:
        #    raise Exception(f"Sweep stop wavelength ({value}) can not be smaller than "
        #                    f"sweep start wavelength ({self.sweep_start_wavelength})!")
        self.laser_config.wl_sweep_stop.set(value)
        self.signals.sweep_stop_wavelength_changed.emit(self.sweep_stop_wavelength)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        self.signals.connected_changed.emit(self.connected)

    @property
    def port(self):
        return self.laser_config.port.get()

    @port.setter
    def port(self, value):
        self.laser_config.port.set(value)
        self.signals.port_changed.emit(self.port)

    @property
    def laser_is_moving(self):
        return self._laser_is_moving

    @laser_is_moving.setter
    def laser_is_moving(self, value: tuple):
        self._laser_is_moving = value[0]
        self.laser_moving_to_wavelength = value[1]
        self.signals.laser_is_moving_changed.emit(self.laser_is_moving, self.laser_moving_to_wavelength)

    @property
    def laser_moving_to_wavelength(self):
        return self._laser_moving_to_wavelength

    @laser_moving_to_wavelength.setter
    def laser_moving_to_wavelength(self, value):
        self._laser_moving_to_wavelength = value
        self.signals.laser_moving_to_wavelength_changed.emit(self.laser_moving_to_wavelength)

    @property
    def current_wavelength(self):
        return self._current_wavelength

    @current_wavelength.setter
    def current_wavelength(self, value):
        self._current_wavelength = value
        self.signals.current_wavelength_changed.emit(self.current_wavelength)

    @property
    def min_laser_wavelength(self):
        return self._min_laser_wavelength

    @min_laser_wavelength.setter
    def min_laser_wavelength(self, value):
        self._min_laser_wavelength = value
        self.signals.min_laser_wavelength_changed.emit(self.min_laser_wavelength)

    @property
    def max_laser_wavelength(self):
        return self._max_laser_wavelength

    @max_laser_wavelength.setter
    def max_laser_wavelength(self, value):
        self._max_laser_wavelength = value
        self.signals.max_laser_wavelength_changed.emit(self.max_laser_wavelength)

    # ==================================================================================================================
    @property
    def deceleration(self):
        return self.laser_config.deceleration.get()

    @deceleration.setter
    def deceleration(self, value):
        self.laser_config.deceleration.set(value)
        self.signals.deceleration_changed.emit(self.deceleration)

    @property
    def min_deceleration(self):
        return self._min_deceleration

    @min_deceleration.setter
    def min_deceleration(self, value):
        self._min_acceleration = value
        self.signals.min_deceleration_changed.emit(self.min_deceleration)

    @property
    def max_deceleration(self):
        return self._max_deceleration

    @max_deceleration.setter
    def max_deceleration(self, value):
        self._max_deceleration = value
        self.signals.max_deceleration_changed.emit(self.max_deceleration)

    # ==================================================================================================================
    @property
    def acceleration(self):
        return self.laser_config.acceleration.get()

    @acceleration.setter
    def acceleration(self, value):
        self.laser_config.acceleration.set(value)
        self.signals.acceleration_changed.emit(self.acceleration)

    @property
    def min_acceleration(self):
        return self._min_acceleration

    @min_acceleration.setter
    def min_acceleration(self, value):
        self._min_acceleration = value
        self.signals.min_acceleration_changed.emit(self.min_acceleration)

    @property
    def max_acceleration(self):
        return self._max_acceleration

    @max_acceleration.setter
    def max_acceleration(self, value):
        self._max_acceleration = value
        self.signals.max_acceleration_changed.emit(self.max_acceleration)

    # ==================================================================================================================

    @property
    def velocity(self):
        return self.laser_config.velocity.get()

    @velocity.setter
    def velocity(self, value):
        self.laser_config.velocity.set(value)
        self.signals.velocity_changed.emit(self.velocity)

    @property
    def min_velocity(self):
        return self._min_acceleration

    @min_velocity.setter
    def min_velocity(self, value):
        self._min_velocity = value
        self.signals.min_velocity_changed.emit(self._min_velocity)

    @property
    def max_velocity(self):
        return self._max_acceleration

    @max_velocity.setter
    def max_velocity(self, value):
        self._max_velocity = value
        self.signals.max_velocity_changed.emit(self._max_velocity)

    # ==================================================================================================================

    @property
    def laser_connected(self):
        return self._laser_connected

    @property
    def wavelength_sweep_running(self):
        return self._wavelength_sweep_running

    @wavelength_sweep_running.setter
    def wavelength_sweep_running(self, value):
        self._wavelength_sweep_running = value
        self.signals.wavelength_sweep_running_changed.emit(self._wavelength_sweep_running)

    # ==================================================================================================================
    @property
    def capturing_device_connected(self):
        return self._capturing_device_connected

    @capturing_device_connected.setter
    def capturing_device_connected(self, value):
        self._capturing_device_connected = value
        self.signals.capturing_device_connected_changed.emit(self.capturing_device_connected)

    @property
    def capturing_device(self) -> captdev.Controller:
        return self._capturing_device

    @capturing_device.setter
    def capturing_device(self, value: captdev.Controller):
        self._capturing_device = value
        self.signals.capturing_device_changed.emit(self._capturing_device)