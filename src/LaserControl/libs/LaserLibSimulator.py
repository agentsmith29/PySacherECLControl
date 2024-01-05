import logging
import time
from random import randint

from LaserControl.libs.LaserSceleton import LaserScelton


class LaserLibSimulator(LaserScelton):
    connected = False

    def __init__(self, logger=None) -> None:
        super().__init__()
        self.pref = "Laser (Simulator)"
        self.port_list = ['Simulator']

        self._connected = False

        self._currentWavelengthPositionIs: float = 0
        self._current_wavelength: float = 857

        self._velocity: float = 1
        self._acceleration: float = 2
        self._deceleration: float = 2

        self.port = "SIM"
        # self.connected = False

        self.logger = logger or logging.getLogger(f"{__name__} (Sim)")
        self.logger.info(f"{self.pref}: Laser Simulator initialized.")

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
        self.logger.debug(f"{self.pref}: Current wavelength position is {self._currentWavelengthPositionIs} nm")
        return self._currentWavelengthPositionIs

    def getCurrentWavelength(self) -> float:
        self.logger.debug(f"{self.pref}: Current wavelength is {self._current_wavelength} nm")
        return self._current_wavelength

    def setVelocity(self, velocity: float) -> None:
        self.logger.info(f"{self.pref}: Velocity set to {velocity} nm/s")
        self._velocity = velocity

    def getVelocity(self) -> float:
        self.logger.debug(f"{self.pref}: Current velocity is {self._velocity} nm/s")
        return self._velocity

    def setAcceleration(self, acceleration: float) -> None:
        self.logger.info(f"{self.pref}: Acceleration set to {acceleration} nm/s^2")
        self._acceleration = acceleration

    def getAcceleration(self) -> float:
        self.logger.debug(f"{self.pref}: Current acceleration is {self._acceleration} nm/s^2")
        return self._acceleration

    def setDeceleration(self, deceleration: float) -> None:
        self.logger.info(f"{self.pref}: Deceleration set to {deceleration} nm/s^2")
        self._deceleration = deceleration

    def getDeceleration(self) -> float:
        self.logger.debug(f"{self.pref}: Current deceleration is {self._deceleration} nm/s^2")
        return self._deceleration

    def getStoredPosition(self, isWvl: bool = True) -> float:
        if isWvl:
            self.logger.debug(f"{self.pref}: Current stored position is {self._current_wavelength} nm")
            return self._current_wavelength
        else:
            self.logger.debug(f"{self.pref}: Current stored position is {self._currentWavelengthPositionIs} steps")
            return self._currentWavelengthPositionIs

    def getOffset(self) -> float:
        self.logger.debug(f"{self.pref}: Current offset is {self._currentWavelengthPositionIs} nm")
        return self._currentWavelengthPositionIs

    def getPositionIs(self) -> float:
        self.logger.debug(f"{self.pref}: Current position is {self._current_wavelength} nm")
        return self._current_wavelength

    def resetPositionIs(self) -> None:
        self.logger.info(f"{self.pref}: Resetting position to 0 nm")
        self._current_wavelength = 0

    # ==================================================================================================================
    # Motor movement functions
    # ==================================================================================================================
    def goToWvl(self, wavelength: float, fast: bool) -> None:
        num_wavelength = int(wavelength)

        #et_acc_dec = self._velocity / self._acceleration
        #wl_after_acc = self._current_wavelength + 0.5 * self._acceleration * et_acc_dec ** 2
        #wl_bevore_dec = num_wavelength - 0.5 * self._deceleration * et_acc_dec ** 2
        #eta = 2 * et_acc_dec + (wl_bevore_dec - wl_after_acc) / self._velocity
        #steps_per_second = (eta / 100)*1000

        print(f"Moving from {self._current_wavelength} to {num_wavelength}")
        if int(self._current_wavelength) > num_wavelength:
            print(f"Going down: {self._current_wavelength} -> {num_wavelength}")
            for i in range(num_wavelength, int(self._current_wavelength), -1):
                print(f"{i} |  ", end="")
                time.sleep(1)
        else:
            print(f"Going up: {self._current_wavelength} -> {num_wavelength}")
            for i in range(int(self._current_wavelength), num_wavelength):
                print(f"{i} |  ", end="")
                time.sleep(1)
        self._current_wavelength = num_wavelength
        print(f"Done: {self._current_wavelength}")

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
