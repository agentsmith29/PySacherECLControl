import logging
import pathlib
import time
from random import randint

from LaserControl.libs.LaserSceleton import LaserScelton
import confighandler as conf


class LaserLibSimulatorConfig(conf.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        self.currentWavelengthPositionIs: conf.Field[float] = conf.Field(0.0,
                                                                          friendly_name="Current wavelength position",
                                                                          description="Current wavelength position in nm")
        self.current_wavelength: conf.Field[float] = conf.Field(857.0, friendly_name="Current wavelength",
                                                                 description="Current wavelength in nm")

        self.velocity: conf.Field[float] = conf.Field(1.0, friendly_name="Velocity",
                                                       description="Velocity in nm/s")
        self.acceleration: conf.Field[float] = conf.Field(2.0, friendly_name="Acceleration",
                                                           description="Acceleration in nm/s^2")
        self.deceleration: conf.Field[float] = conf.Field(2.0, friendly_name="Deceleration",
                                                           description="Deceleration in nm/s^2")

        self.register()


class LaserLibSimulator(LaserScelton):
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

        #self._currentWavelengthPositionIs: float = 0
        #self._current_wavelength: float = 857

        #self._velocity: float = 1
        #self._acceleration: float = 2
        #self._deceleration: float = 2

        self.port = "SIM"
        # self.connected = False

        self.logger = logger or logging.getLogger(f"{__name__} (Sim)")
        self.logger.info(f"{self.pref}: Laser Simulator initialized.")

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
    # Connection functions
    # ==================================================================================================================
    def connectMotor(self, port: str = "USB0") -> None:
        if self.connected:
            raise Exception("Already connected to Laser Simulator")
        self.logger.debug(f"{self.pref}: Connecting to Laser Simulator.")
        time.sleep(randint(1, 2))
        self._connected = True
        self.logger.info(f"{self.pref}: Connected to Laser Simulator.")

    def closeMotorConnection(self) -> None:
        self.logger.info(f"{self.pref}: Disconnecting from Laser Simulator")
        self._connected = False

    # ==================================================================================================================
    # Motor Position functions
    # ==================================================================================================================
    def getcurrentWavelengthPositionIs(self) -> float:
        self.logger.debug(f"{self.pref}: Current wavelength position is {self.currentWaveLengthPositionIs} nm")
        return self.currentWaveLengthPositionIs

    def getCurrentWavelength(self) -> float:
        self.logger.debug(f"{self.pref}: Current wavelength is {self.currentWavelength} nm")
        return self.currentWavelength

    def setVelocity(self, velocity: float) -> None:
        self.logger.info(f"{self.pref}: Velocity set to {velocity} nm/s")
        self.velocity = velocity

    def getVelocity(self) -> float:
        self.logger.debug(f"{self.pref}: Current velocity is {self.velocity} nm/s")
        return self.velocity

    def setAcceleration(self, acceleration: float) -> None:
        self.logger.info(f"{self.pref}: Acceleration set to {acceleration} nm/s^2")
        self.acceleration = acceleration

    def getAcceleration(self) -> float:
        self.logger.debug(f"{self.pref}: Current acceleration is {self.acceleration} nm/s^2")
        return self.acceleration

    def setDeceleration(self, deceleration: float) -> None:
        self.logger.info(f"{self.pref}: Deceleration set to {deceleration} nm/s^2")
        self.deceleration = deceleration

    def getDeceleration(self) -> float:
        self.logger.debug(f"{self.pref}: Current deceleration is {self.deceleration} nm/s^2")
        return self.deceleration

    def getStoredPosition(self, isWvl: bool = True) -> float:
        if isWvl:
            self.logger.debug(f"{self.pref}: Current stored position is {self._current_wavelength} nm")
            return self._current_wavelength
        else:
            self.logger.debug(f"{self.pref}: Current stored position is {self.currentWaveLengthPositionIs} steps")
            return self.currentWaveLengthPositionIs

    def getOffset(self) -> float:
        self.logger.debug(f"{self.pref}: Current offset is {self.currentWaveLengthPositionIs} nm")
        return self.currentWaveLengthPositionIs

    def getPositionIs(self) -> float:
        self.logger.debug(f"{self.pref}: Current position is {self.currentWavelength} nm")
        return self.currentWavelength

    def resetPositionIs(self) -> None:
        self.logger.info(f"{self.pref}: Resetting position to 0 nm")
        self.currentWavelength = 0

    # ==================================================================================================================
    # Motor movement functions
    # ==================================================================================================================
    def goToWvl(self, wavelength: float, fast: bool) -> None:
        num_wavelength = int(wavelength)

        # et_acc_dec = self._velocity / self._acceleration
        # wl_after_acc = self._current_wavelength + 0.5 * self._acceleration * et_acc_dec ** 2
        # wl_bevore_dec = num_wavelength - 0.5 * self._deceleration * et_acc_dec ** 2
        # eta = 2 * et_acc_dec + (wl_bevore_dec - wl_after_acc) / self._velocity
        # steps_per_second = (eta / 100)*1000

        print(f"Moving from {self.currentWavelength} to {num_wavelength}")
        if int(self.currentWavelength) > num_wavelength:
            print(f"Going down: {self.currentWavelength} -> {num_wavelength}")
            for i in range(int(self.currentWavelength), num_wavelength, -1):
                print(f"{i} |  ", end="")
                time.sleep(1)
        else:
            print(f"Going up: {self.currentWavelength} -> {num_wavelength}")
            for i in range(int(self.currentWavelength), num_wavelength):
                print(f"{i} |  ", end="")
                time.sleep(1)
        self.currentWavelength = num_wavelength
        print(f"Done: {self.currentWavelength}")

    def startScan(self, wavelength: float, target: float) -> None:
        self.goToWvl(wavelength, True)
        self.goToWvl(target, True)

    # ==================================================================================================================
    # Calibration functions#
    # ==================================================================================================================
    def Calibrate(self, wavelength: float) -> None:
        self.logger.info(f"{self.pref}: Calibrating to {wavelength} nm")

    # ==================================================================================================================
    # Auxiliary functions, which read or store variables in the code and on the EPOS board.
    # ==================================================================================================================
    def setStartWvl(self, wavelength: float) -> None:
        self.logger.info(f"{self.pref}: Setting start wavelength to {wavelength} nm")
        self._current_wavelength = wavelength

    def getStartWvl(self) -> float:
        self.logger.info(f"{self.pref}: Start wavelength is {self._current_wavelength} nm")
        return self._current_wavelength

    def setTargetWvl(self, wavelength: float) -> None:
        self.logger.info(f"{self.pref}: Setting target wavelength to {wavelength} nm")
        self._current_wavelength = wavelength

    def getTargetWvl(self) -> float:
        self.logger.info(f"{self.pref}: Target wavelength is {self._current_wavelength} nm")
        return self._current_wavelength
