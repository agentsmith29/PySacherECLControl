import os
import pathlib
import time
from multiprocessing import Value

import cmp
from cmp.CProperty import CProperty

# from LaserControl.controller.LaserCon import LaserCon
dir = pathlib.Path(f"{os.path.dirname(os.path.realpath(__file__))}/../../libs")
dir = str(dir.resolve())

# Copy the dll to the startup directory



from LaserControl.libs import SacherMotorControl as LaserLib


class MPLaserDevice(cmp.CProcess):

    def __init__(self, state_queue, cmd_queue,
                 laser_moving_flag: Value,
                 laser_finished_flag: Value,
                 start_capture_flag: Value,
                 kill_flag: Value,
                 internal_log, internal_log_level, log_file):
        super().__init__(state_queue, cmd_queue,
                         kill_flag=kill_flag,
                         internal_log=internal_log, internal_log_level=internal_log_level, log_file=log_file)

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
        self.laser = LaserLib.Motor()

    @cmp.CProcess.register_signal()
    def dev_connect(self, usb_port: str) -> bool:
        """
        Connect to the laser on the specified USB port.
        :param usb_port: USB port to connect to
        :return: True if connected, False otherwise
        """
        self.logger.info(f"Connecting to laser on port {usb_port}")
        self.read_laser_settings()
        try:
            self.laser.connect(usb_port)
            self.connected = True
        except Exception as e:
            self.logger.error(f"Error connecting to laser: {e}")
            self.connected = False

            raise e



        return self._connected

    @CProperty
    def min_wavelength(self):
        return self._min_wavelength

    @CProperty
    def max_wavelength(self):
        return self._max_wavelength






    @CProperty
    def wavelength_sweep_running(self):
        return self._wavelength_sweep_running

    @wavelength_sweep_running.setter('wavelength_sweep_running_changed')
    def wavelength_sweep_running(self, value: bool):
        self._wavelength_sweep_running = value


    @CProperty
    def connected(self):
        return self._connected

    @connected.setter('connected_changed')
    def connected(self, value: float):
        self._connected = value

    # ==================================================================================================================

    @CProperty
    def current_wavelength(self):
        return self._current_wavelength

    @current_wavelength.setter('current_wavelength_changed')
    def current_wavelength(self, value: float):
        self._current_wavelength = value

    @CProperty
    def min_wavelength(self):
        return self._min_wavelength

    @min_wavelength.setter('min_wavelength_changed')
    def min_wavelength(self, value: float):
        self._min_wavelength = value

    # ==================================================================================================================

    @CProperty
    def max_wavelength(self):
        return self._max_wavelength

    @max_wavelength.setter('max_wavelength_changed')
    def max_wavelength(self, value: float):
        self._max_wavelength = value

    # ==================================================================================================================

    @CProperty
    def velocity(self):
        return self._velocity

    @velocity.setter('velocity_changed')
    def velocity(self, value: float):
        self._velocity = value

    # ==================================================================================================================

    @CProperty
    def acceleration(self):
        return self._acceleration

    @acceleration.setter('acceleration_changed')
    def acceleration(self, value: float):
        self._acceleration = value

    # ==================================================================================================================

    @CProperty
    def deceleration(self):
        return self._deceleration

    @deceleration.setter('deceleration_changed')
    def deceleration(self, value: float):
        self._deceleration = value





    def read_current_wavelength(self) -> float:
        if self.laser is None or self._connected is False:
            self.current_wavelength = 0
            return -1
        else:
            self.current_wavelength = float(self.laser.getWavelength())
        return self._current_wavelength


    def read_min_wavelength(self) -> float:
        if self.laser is None or self._connected is False:
            self.min_wavelength = 0
            return -1
        else:
            self.min_wavelength = float(self.laser.getWavelengthMinMax()[0])

        return self._min_wavelength

    def read_max_wavelength(self) -> float:
        if self.laser is None or self._connected is False:
            self.max_wavelength = 0
            return -1
        else:
            self.max_wavelength = float(self.laser.getWavelengthMinMax()[1])
        return self._max_wavelength

    def read_velocity(self) -> float:
        if self.laser is None or self._connected is False:
            self.velocity = 0
            return -1
        else:
            self.velocity = float(self.laser.getVelocity()[0])
        return self._velocity

    def read_acceleration(self) -> float:
        if self.laser is None or self._connected is False:
            self.acceleration = 0
            return -1
        else:
            self.acceleration = float(self.laser.getVelocity()[1])
        return self._acceleration

    def read_deceleration(self) -> float:
        if self.laser is None or self._connected is False:
            self.deceleration = 0
            return -1
        else:
            self.deceleration = float(self.laser.getVelocity()[2])
        return self._deceleration


    def read_laser_settings(self, usb_port: str = None, *args, **kwargs):
        self.logger.info(f"Reading laser settings.")

        self.read_current_wavelength()
        self.read_min_wavelength()
        self.read_max_wavelength()
        self.read_velocity()
        self.read_acceleration()
        self.read_deceleration()


    @CProperty
    def laser_is_moving(self):
        return self._laser_moving

    @laser_is_moving.setter('laser_is_moving_changed')
    def laser_is_moving(self, value: tuple):
        self.laser_moving_flag.value = int(value[0])
        self._laser_moving = value



    @cmp.CProcess.register_signal(postfix="_changed")
    def movement_finished(self, finished: bool):
        self.laser_finished_flag.value = finished
        return self.laser_finished_flag.value

    @cmp.CProcess.register_signal(postfix="_finished")
    def move_to_wavelength(self, usb_port: str = None,
                           wavelength: float = None, capture: bool = False, *args, **kwargs):

        if self.laser is None or self._connected is False:
            return -1
        else:


            self.read_laser_settings()
            self.laser_is_moving = (False, wavelength)
            self.laser_finished_flag.value = False
            self.logger.info(f"**** Go to selected wavelength. Started moving laser to {wavelength}. ****")
            time_start = time.time()
            self.laser_is_moving = (True, wavelength)
            if capture:
                self.start_capture_flag.value = int(True)
                self.logger.info(
                    f"******************** Capture flag set to {self.start_capture_flag.value} **********************")

            time.sleep(1)
            self.laser.moveToWavelength(wavelength, False)
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
                f">>> Current Wavelength: {self.read_current_wavelength()}. Took {time_end - time_start} seconds to move.")
            self.read_laser_settings()
            # laser_connected_flag.value = False  # We need to manually set this
            return self.read_current_wavelength()


    def wavelength_sweep(self, usb_port: str = None,
                         wavelength_start: float = None,
                         wavelength_end: float = None, *args, **kwargs):

        # laser_finished_flag.value = False
        # laser_state.value.connected = False
        self.wavelength_sweep_running = True
        self.read_laser_settings(usb_port)
        self.logger.info(f"Starting sweep from {wavelength_start} to {wavelength_end}.")
        self.logger.info(f"Resetting laser to start wavelength {wavelength_start}. "
                         f"Current wavelength is {self.current_wavelength}")
        self.move_to_wavelength(usb_port, wavelength_start)
        self.logger.info(f"Starting sweep from {wavelength_start} to {wavelength_end}.")
        self.move_to_wavelength(usb_port, wavelength_end, capture=True)
        self.logger.info(f"Finished sweep from {wavelength_start} to {wavelength_end}.")
        self.wavelength_sweep_running = False
        # laser_state.connected = False
