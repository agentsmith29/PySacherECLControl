import logging
import pathlib
import time
from random import randint

from SacherECLControl.libs.LaserSceleton import LaserScelton
import confPy6 as conf


class LaserLibSimulatorConfig(conf.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        self.currentWavelengthPositionIs: conf.Field[float] = conf.Field(0.0,
                                                                          friendly_name="Current wavelength position",
                                                                          description="Current wavelength position in nm")

        self.current_wavelength: conf.Field[float] = conf.Field(857.0, friendly_name="Current wavelength",
                                                                 description="Current wavelength in nm")

        self.min_wavelength: conf.Field[float] = conf.Field(830.0, friendly_name="Min wavelength",
                                                                description="Minimum wavelength in nm")

        self.max_wavelength: conf.Field[float] = conf.Field(880.0, friendly_name="Max wavelength",
                                                                description="Maximum wavelength in nm")

        self.velocity: conf.Field[float] = conf.Field(1.0, friendly_name="Velocity",
                                                       description="Velocity in nm/s")
        self.acceleration: conf.Field[float] = conf.Field(2.0, friendly_name="Acceleration",
                                                           description="Acceleration in nm/s^2")
        self.deceleration: conf.Field[float] = conf.Field(2.0, friendly_name="Deceleration",
                                                           description="Deceleration in nm/s^2")

        self.register()


# Implements the Simulator for Version
class Motor(LaserScelton):
    connected = False

    def __init__(self, logger=None) -> None:
        super().__init__()
        self.pref = "Laser (Simulator)"
        self.port_list = ['Simulator']

        self._connected = False

        pconfath = ".sim/laser_simulator.yaml"
        self.conf = LaserLibSimulatorConfig()
        self.conf.autosave(enable=True, path=pconfath)

        # check if .sim/laser_simulator.yaml exists
        if pathlib.Path(pconfath).exists():
            self.conf.load(pconfath, True)

        self.conf.module_log_enabled = True
        self.conf.module_log_level = logging.DEBUG

        self.port = "SIM"
        # self.connected = False

        self.logger = logger or logging.getLogger(f"{__name__} (Sim)")
        self.logger.info(f"{self.pref}: Laser Simulator initialized.")

    # ==================================================================================================================
    @property
    def currentWaveLengthPositionIs(self) -> float:
        return self.conf.currentWavelengthPositionIs.get()

    @currentWaveLengthPositionIs.setter
    def currentWaveLengthPositionIs(self, value: float) -> None:
        self.conf.currentWavelengthPositionIs.set(value)

    @property
    def currentWavelength(self) -> float:
        return self.conf.current_wavelength.get()

    @currentWavelength.setter
    def currentWavelength(self, value: float) -> None:
        self.conf.current_wavelength.set(value)

    @property
    def velocity(self) -> float:
        return self.conf.velocity.get()

    @velocity.setter
    def velocity(self, value: float) -> None:
        self.conf.velocity.set(value)

    @property
    def acceleration(self) -> float:
        return self.conf.acceleration.get()

    @acceleration.setter
    def acceleration(self, value: float) -> None:
        self.conf.acceleration.set(value)

    @property
    def deceleration(self) -> float:
        return self.conf.deceleration.get()

    @deceleration.setter
    def deceleration(self, value: float) -> None:
        self.conf.deceleration.set(value)

    # ==================================================================================================================

    # ==================================================================================================================
    # Connection functions
    # ==================================================================================================================
    def connect(self, port: str = "USB0") -> None:
        """
        Establishes a connection to the Epos and reads all the needed data saved on the internal
        registry.
        :param port: usb port on which the connection should be established, default=’USB0’
        :return: None
        """
        if self.connected:
            raise Exception("Already connected to Laser Simulator")
        self.logger.debug(f"{self.pref}: Connecting to Laser Simulator.")
        time.sleep(randint(1, 2))
        self._connected = True
        self.logger.info(f"{self.pref}: Connected to Laser Simulator.")

    def disconnect(self) -> None:
        """
        Closes the connection to the Epos.
        :return:
        """
        self.logger.info(f"{self.pref}: Disconnecting from Laser Simulator")
        self._connected = False

    # ==================================================================================================================
    # Laser information/status functions
    # ==================================================================================================================

    def getWavelength(self) -> float:
        """
        Returns the wavelength from the current motor position stored on the epos.
        :return: Wavelength in nm (float)
        """
        self.logger.debug(f"{self.pref}: Current wavelength is {self.currentWavelength} nm")
        return self.currentWavelength

    def getWavelengthMinMax(self) -> tuple:
        """
        Return the minimum and maximum wavelength of the system.
        :return: tuple(float,float) minimum wavelength, maximum wavelength
        """
        self.logger.debug(f"{self.pref}: Min/Max wavelength "
                          f"{self.conf.min_wavelength.get()}/{self.conf.min_wavelength.get()} nm")
        return self.conf.min_wavelength.get(), self.conf.max_wavelength.get()

    def setVelocityParameter(self, velocity: float, acceleration: float, deceleration) -> None:
        """
         Sets the velocity parameters on the Epos.
        :param velocity:  velocity of the system in nm/s
        :param acceleration: acceleration of the system in nm/s2
        :param deceleration: deceleration of the system in nm/s2
        :return: None
        """

        self.logger.info(f"{self.pref}:  set to {acceleration} nm/s^2")
        self.logger.info(f"{self.pref}: Deceleration set to {deceleration} nm/s^2")
        self.velocity = velocity
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.logger.info(f"{self.pref}: Velocity/acceleration/deceleration set to "
                         f"{velocity}(nm/s)/{acceleration}(nm/s^2)/{deceleration}(nm/s^2)")

    def getVelocityParameter(self) -> tuple:
        """
        Returns the velocity in nm/s, acceleration and deceleration in nm/s2 stored on the
        :return: tuple(float, float, float) velocity, acceleration, deceleration
        """
        self.logger.info(f"{self.pref}: Current velocity/acceleration/deceleration set to "
                         f"{self.velocity}(nm/s)/{self.acceleration}(nm/s^2)/{self.deceleration}(nm/s^2)")
        return (self.velocity, self.acceleration, self.deceleration)

    def getMoving(self) -> bool:
        """
        Returns true or false whether the motor is moving or not.
        :return: True, if moving, false otherwise
        """

    # =================================================================================================================
    # Movement functions
    # =================================================================================================================
    def moveToWavelength(self, wavelength: float, highPrecision: bool, trigger: int) -> None:
        """
        Moves the Motor to a given Wavelength.
        :param wavelength: The wavelength to move to given in nm
        :param highPrecision: High Precision Mode activated. When the relative movement is negative the Motor
        drives 10000 steps below the goal to always come up to it with a positive movement.
        If using a ballscrew system the steps will be reduced to 3000.
        :param trigger:
            0 - no trigger activated
            1 - Position Compare trigger activated
            2 - Motion trigger activated
        :return: None
        """

        num_wavelength = int(wavelength)

        #def calcMovementTime():
        #    et_acc_dec = self.velocity / self.acceleration
        #    wl_after_acc = self.currentWavelength + 0.5 * self.acceleration * et_acc_dec ** 2
        #    wl_before_dec = num_wavelength - 0.5 * self.deceleration * et_acc_dec ** 2
        #    eta = 2 * et_acc_dec + (wl_before_dec - wl_after_acc) / self.velocity
        #    # laser need eta in ms
        #    steps_per_second = (eta / 100)*1000
        #    return steps_per_second

        print(f"Moving from {self.currentWavelength} to {num_wavelength}")
        if int(self.currentWavelength) > num_wavelength:
            print(f"Going down: {self.currentWavelength} -> {num_wavelength}")
            for i in range(int(self.currentWavelength)*10, num_wavelength*10, -int(self.velocity)):
                print(f"{i/10} |  ", end="")
                time.sleep(0.1)
        else:
            print(f"Going up: {self.currentWavelength} -> {num_wavelength}")
            for i in range(int(self.currentWavelength)*10, num_wavelength*10, int(self.velocity)):
                print(f"{i/10} |  ", end="")
                time.sleep(0.1)
        self.currentWavelength = num_wavelength
        print(f"Done: {self.currentWavelength}")

    def moveSteps(self, steps: int, trigger: int) -> None:
        """
        Moves A certain amount of steps up to 10000 in either direction.
        Parameter:
        :param steps: Number of steps to move (int)
        :param trigger: (int)
                    0 - no trigger activated
                    1 - Position Compare trigger activated
                    2 - Motion trigger activated
        :return: None
        """
        self.logger.info(f"{self.pref}: Moving {steps} steps")

    def stopMovement(self) -> None:
        """
        Stops the movement of the motor.
        :return: None
        """
        self.logger.info(f"{self.pref}: Stopping movement")

    # ==================================================================================================================
    # Calibration functions#
    # ==================================================================================================================
    def calibrate(self, wavelength: float) -> None:
        """
        Sets the current motor position to the wavelength position according to the given wavelength.
        :param wavelength (float): wavelength in nm to calibrate the system
        :return: None
        """
        self.logger.info(f"{self.pref}: Calibrating to {wavelength} nm")

    # ==================================================================================================================
    # Trigger Methods
    # ==================================================================================================================

    def triggerParameter(self, intervalWidth) -> None:
        """
        Sets the parameters for the position compare trigger
        :param intervalWidth: Interval width for the trigger signal in nm
        :return: None
        """
        self.logger.info(f"{self.pref}: Setting trigger parameter to {intervalWidth} nm")

    def reverseMotionTrigger(self) -> None:
        """
        Reverses the digital output for MotionTrigger. To change between active while moving
        or active while standing.
        """
        self.logger.info(f"{self.pref}: Reversing Motion Trigger")

