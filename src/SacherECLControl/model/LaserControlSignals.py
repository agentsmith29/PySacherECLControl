from PySide6.QtCore import QObject, Signal


class LaserControlSignals(QObject):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


    laser_config_changed = Signal()

    # Device status
    connected_changed = Signal(bool)
    port_changed = Signal(str)

    # Device parameter
    laser_moving_to_wavelength_changed = Signal(float)

    current_wavelength_changed = Signal(float)
    min_laser_wavelength_changed = Signal(float)
    max_laser_wavelength_changed = Signal(float)

    deceleration_changed = Signal(float)
    min_deceleration_changed = Signal(float)
    max_deceleration_changed = Signal(float)

    acceleration_changed = Signal(float)
    min_acceleration_changed = Signal(float)
    max_acceleration_changed = Signal(float)


    velocity_changed = Signal(float)
    min_velocity_changed = Signal(float)
    max_velocity_changed = Signal(float)


    laser_is_moving_changed = Signal(bool, float)
    wavelength_sweep_running_changed = Signal(bool)
    laser_at_position_changed = Signal(bool)
    laser_ready_for_sweep_changed = Signal(bool)

    # Device sweep parameter
    sweep_start_wavelength_changed = Signal(float)
    sweep_stop_wavelength_changed = Signal(float)

    connected = Signal(bool)

    capturing_device_changed = Signal(bool)
    capturing_device_connected_changed = Signal(object)

    # current wavelength, min wavelength, max wavelength
    # velocity, acceleration, deceleration
    current_speed_settings = Signal(float, float, float)
    wavelength_sweep_finished = Signal(bool)
    error = Signal(str)
    in_wavelength_sweep_start = Signal(bool)
