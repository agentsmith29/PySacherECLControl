import os
import pathlib
import sys
import time
from multiprocessing import Value

import mpPy6
from mpPy6.CProperty import CProperty

from SacherECLControl import Helpers, __rootdir__

# Copy the dll to the startup directory

try:
    spath = str(pathlib.Path(os.getenv("MOTOR_CONTROL_PYD")).absolute().parent.as_posix())
    sys.path.append(spath)
    import SacherMotorControl as LaserLib

except Exception as e:
    print(f"Warning: Could not import SacherMotorControl: {e}. Using LaserLibSimulator instead.")
    from SacherECLControl.libs import LaserLibSimulator as LaserLib


#from SacherECLControl.libs import LaserLibSimulator as LaserLib


class MPLaserDevice(mpPy6.CProcess):

    def __init__(self, state_queue, cmd_queue,
                 laser_moving_flag: Value,
                 laser_finished_flag: Value,
                 start_capture_flag: Value,
                 dll_copy_path,
                 kill_flag: Value,
                 internal_log, internal_log_level, log_file):
        super().__init__(state_queue, cmd_queue,
                         kill_flag=kill_flag,
                         internal_log=internal_log, internal_log_level=internal_log_level, log_file=log_file)


        self.dll_copy_path = dll_copy_path
        #import importlib.util
        #import sys
        #spec = importlib.util.spec_from_file_location(module_name, module_name_path)
        #foo = importlib.util.module_from_spec(spec)
        #sys.modules[module_name] = foo
        #spec.loader.exec_module(foo)

        # if not self.logger.handlers:
        #     self.logger.setLevel(level=logging.DEBUG)
        # self.logger.disabled = False
        # print(self.logger)
        # self.logger.info(f"Created logger for {self.__class__.__name__}({os.getpid()})")
        self._connected = False
        self._current_wavelength = -1

        self._min_wavelength = 0
        self._max_wavelength = 0
        self._velocity = 0
        self._acceleration = 0
        self._deceleration = 0

        self._laser_moving = False

        self.laser_moving_flag = laser_moving_flag
        self.laser_finished_flag = laser_finished_flag
        self.start_capture_flag = start_capture_flag

        self._wavelength_sweep_running = False

    def postrun_init(self):
        try:
            self.logger.info(f"Copying DLL to {self.dll_copy_path}")
            Helpers.copyEposDLL(f"{self.dll_copy_path}", logger=self.logger)
        except Exception as e:
            self.logger.error(f"Error copying DLL: {e}")
        self.laser = LaserLib.Motor()
    # ==================================================================================================================
    # Properties
    # ==================================================================================================================
    @CProperty
    def connected(self):
        """ Returns if the laser is connected. """
        return self._connected

    @connected.setter('connected_changed')
    def connected(self, value: float):
        """ Sets the connected state of the laser. Only used internally by the process. """
        self._connected = value

    @CProperty
    def current_wavelength(self):
        """
        Returns the wavelength from the current motor position stored on the epos
        """
        return self._current_wavelength

    @current_wavelength.setter('current_wavelength_changed')
    def current_wavelength(self, value: float):
        """
        Sets the current wavelength of the laser. Only used internally by the process.
        :param value: Wavelength read by the laser library
        """
        self._current_wavelength = value

    @CProperty
    def min_wavelength(self):
        """
        :return: Returns the minimum wavelength the laser can be set to.
        """
        return self._min_wavelength

    @min_wavelength.setter('min_wavelength_changed')
    def min_wavelength(self, value: float):
        """
        Sets the minimum wavelength of the laser. Only used internally by the process.
        :param value: The minimum wavelength read by the laser library
        :return:
        """
        self._min_wavelength = value

    @CProperty
    def max_wavelength(self):
        """
        :return: Returns the maximum wavelength the laser can be set to.
        """
        return self._max_wavelength

    @max_wavelength.setter('max_wavelength_changed')
    def max_wavelength(self, value: float):
        """ Sets the maximum wavelength of the laser. Only used internally by the process."""
        self._max_wavelength = value

    @CProperty
    def velocity(self):
        """
        :return: Returns the velocity of the laser.
        :return:
        """
        return self._velocity

    @velocity.setter('velocity_changed')
    def velocity(self, value: float):
        """ Sets the velocity of the laser. Only used internally by the process."""
        self._velocity = value

    @CProperty
    def acceleration(self):
        """
        :return: Returns the acceleration of the laser.
        :return:
        """
        return self._acceleration

    @acceleration.setter('acceleration_changed')
    def acceleration(self, value: float):
        """
        Sets the acceleration of the laser. Only used internally by the process.
        :param value:
        :return:
        """
        self._acceleration = value

    # ==================================================================================================================

    @CProperty
    def deceleration(self):
        """
        :return: Returns the deceleration of the laser.
        :return:
        """
        return self._deceleration

    @deceleration.setter('deceleration_changed')
    def deceleration(self, value: float):
        """
        Sets the deceleration of the laser. Only used internally by the process.
        :param value:
        :return:
        """
        self._deceleration = value

    # ==================================================================================================================
    # Connection
    # ==================================================================================================================
    @mpPy6.CProcess.register_signal()
    def connect_device(self, usb_port: str) -> bool:
        """
        Connect to the laser on the specified USB port.
        :param usb_port: USB port to connect to
        :return: True if connected, False otherwise
        """
        self.logger.info(f"Connecting to laser on port {usb_port}")

        try:
            self.laser.connect(usb_port)
            self.connected = True
        except Exception as e:
            self.logger.error(f"Error connecting to laser: {e}")
            self.connected = False
            raise e

        self.get_laser_settings()
        return self._connected

    @mpPy6.CProcess.register_signal()
    def disconnect_device(self) -> bool:
        """
        Closes the connection to the Epos.
        """
        self.logger.info(f"Disconnecting from laser.")

        try:
            self.laser.disconnect()
            self.connected = False
        except Exception as e:
            self.logger.error(f"Error disconnecting from laser: {e}")
            self.connected = False
            raise e

        self.get_laser_settings()
        return self._connected

    # ==================================================================================================================#
    #
    # ==================================================================================================================#
    @CProperty
    def wavelength_sweep_running(self):
        return self._wavelength_sweep_running

    @wavelength_sweep_running.setter('wavelength_sweep_running_changed')
    def wavelength_sweep_running(self, value: bool):
        self._wavelength_sweep_running = value

    # ==================================================================================================================

    # ==================================================================================================================

    def _check_laser_state(self) -> bool:
        """
        Check if the laser is connected and the laser object is initialized.
        This is a helper function to avoid code duplication.
        :param func:
        :return:
        """
        if self.laser is None or self._connected is False:
            return False
        else:
            return True

    # ==================================================================================================================

    # ==================================================================================================================
    # Reading functions. Updates the laser settings of this class.
    # ==================================================================================================================
    def get_current_wavelength(self) -> float:
        if self.laser is None or self._connected is False:
            self.current_wavelength = 0
            return -1
        else:
            self.current_wavelength = float(self.laser.getWavelength())
        return self._current_wavelength

    def get_min_wavelength(self) -> float:
        if self.laser is None or self._connected is False:
            self.min_wavelength = 0
            return -1
        else:
            self.min_wavelength = float(self.laser.getWavelengthMinMax()[0])

        return self._min_wavelength

    def get_max_wavelength(self) -> float:
        if self.laser is None or self._connected is False:
            self.max_wavelength = 0
            return -1
        else:
            self.max_wavelength = float(self.laser.getWavelengthMinMax()[1])
        return self._max_wavelength

    def get_velocity(self) -> float:
        if self.laser is None or self._connected is False:
            self.velocity = 0
            return -1
        else:
            self.velocity = float(self.laser.getVelocityParameter()[0])
        return self._velocity

    @mpPy6.CProcess.register_signal()
    def set_velocity(self, velocity: float) -> None:
        """ Set the velocity of the laser. """
        if self._check_laser_state():
            self.laser.setVelocityParameter(velocity, self._acceleration, self._deceleration)
            self.get_laser_settings()
        else:
            raise Exception("Velocity could not be set. Laser is not connected.")

    def get_acceleration(self) -> float:
        if self.laser is None or self._connected is False:
            self.acceleration = 0
            return -1
        else:
            self.acceleration = float(self.laser.getVelocityParameter()[1])
        return self._acceleration

    @mpPy6.CProcess.register_signal()
    def set_acceleration(self, acceleration: float) -> None:
        """ Set the acceleration of the laser. """
        if self._check_laser_state():
            self.laser.setVelocityParameter(self._velocity, acceleration, self._deceleration)
            self.get_laser_settings()
        else:
            raise Exception("Acceleration could not be set. Laser is not connected.")

    def get_deceleration(self) -> float:
        if self.laser is None or self._connected is False:
            self.deceleration = 0
            return -1
        else:
            self.deceleration = float(self.laser.getVelocityParameter()[2])
        return self._deceleration

    @mpPy6.CProcess.register_signal()
    def set_deceleration(self, deceleration: float) -> None:
        """ Set the deceleration of the laser. """
        if self._check_laser_state():
            self.laser.setVelocityParameter(self._velocity, self._acceleration, deceleration)
            self.get_laser_settings()
        else:
            raise Exception("Deceleration could not be set. Laser is not connected.")

    @mpPy6.CProcess.register_signal(signal_name="laser_settings_changed")
    def get_laser_settings(self, *args, **kwargs):
        self.logger.info(f"Reading laser settings.")

        self.get_min_wavelength()
        self.get_max_wavelength()
        self.get_current_wavelength()
        self.get_velocity()
        self.get_acceleration()
        self.get_deceleration()

    @CProperty
    def laser_is_moving(self):
        return self._laser_moving

    @laser_is_moving.setter('laser_is_moving_changed')
    def laser_is_moving(self, value: tuple):
        self.laser_moving_flag.value = int(value[0])
        self._laser_moving = value

    @mpPy6.CProcess.register_signal(postfix="_changed")
    def movement_finished(self, finished: bool):
        self.laser_finished_flag.value = finished
        return self.laser_finished_flag.value

    @mpPy6.CProcess.register_signal(postfix="_finished")
    def move_to_wavelength(self, usb_port: str = None,
                           wavelength: float = None, capture: bool = False, *args, **kwargs):

        if self.laser is None or self._connected is False:
            return -1
        else:

            self.get_laser_settings()
            self.laser_is_moving = (False, wavelength)
            self.laser_finished_flag.value = False
            self.logger.info(f"**** Go to selected wavelength. Started moving laser to {wavelength}. ****")
            time_start = time.time()
            self.laser_is_moving = (True, wavelength)
            if capture:
                self.start_capture_flag.value = int(True)
                self.logger.info(
                    f"******************** Capture flag set to {self.start_capture_flag.value} **********************")

            #time.sleep(1)
            self.laser.moveToWavelength(wavelength, False, trigger=0)
            self.start_capture_flag.value = int(False)
            self._module_logger.info(
                f"******************** Capture flag set to {self.start_capture_flag.value} **********************")
            self.laser_is_moving = (False, wavelength)
            time_end = time.time()
            # if capture_device_started_flag is not None:
            #    capture_device_started_flag.value = False
            # laser_finished_flag.value = True
            # laser_moving_flag.value = False
            self.logger.info(f"Go to selected wavelength finished.")

            # current_wavelength.value = con.current_wavelength
            self.logger.info(
                f">>> Current Wavelength: {self.get_current_wavelength()}. Took {time_end - time_start} seconds to move.")
            self.get_laser_settings()
            # laser_connected_flag.value = False  # We need to manually set this
            return self.get_current_wavelength()

    def wavelength_sweep(self, usb_port: str = None,
                         wavelength_start: float = None,
                         wavelength_end: float = None, *args, **kwargs):

        # laser_finished_flag.value = False
        # laser_state.value.connected = False
        self.wavelength_sweep_running = True
        self.get_laser_settings(usb_port)
        self.logger.info(f"Starting sweep from {wavelength_start} to {wavelength_end}.")
        self.logger.info(f"Resetting laser to start wavelength {wavelength_start}. "
                         f"Current wavelength is {self.current_wavelength}")
        self.move_to_wavelength(usb_port, wavelength_start)
        self.logger.info(f"Starting sweep from {wavelength_start} to {wavelength_end}.")
        self.move_to_wavelength(usb_port, wavelength_end, capture=True)
        self.logger.info(f"Finished sweep from {wavelength_start} to {wavelength_end}.")
        self.wavelength_sweep_running = False
        # laser_state.connected = False
