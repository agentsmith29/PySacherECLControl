class LaserScelton():

    # ==================================================================================================================
    # Connection functions
    # ==================================================================================================================
    def connectMotor(self, port: str = "USB0") -> None:
        """
        Connects EPOS motor at the given port
        :param port: Port of the USB connect (USB0, USB1, USB2, USB3, ...)
        """
        raise NotImplementedError()

    def closeMotorConnection(self) -> None:
        """
        Closes EPOS motor connection
        :return:
        """
        raise NotImplementedError()

    # ==================================================================================================================
    # Motor Position functions
    # ==================================================================================================================
    def getcurrentWavelengthPositionIs(self) -> float:
        """
        Returns calculated wavelength in nm. This function returns the actual wavelength calculated from the
        real motor position (not the value stored in the motor memory).
        Returns the current encoder position and is therefore a stronger indication that the motor is actually moving.
        Values of "getCurrentWavelength" and "getcurrentWavelengthPositionIs" can differ between 1 to 2 positions,
        after the calibration has been performed.
        :return: calculated wavelength in nm (float)
       """
        raise NotImplementedError()

    def getCurrentWavelength(self) -> float:
        """
        Returns stored wavelength in nm.
        :return: stored wavelength in nm (float)
        """
        raise NotImplementedError()

    def setVelocity(self, velocity: float) -> None:
        """
        Sets the velocity in nm/s
        :param velocity: velocity in nm/s
        :return: None
        """
        raise NotImplementedError()

    def getVelocity(self) -> float:
        """
        Returns velocity in nm/s
        :return:
        """
        raise NotImplementedError()

    def setAcceleration(self, acceleration: float) -> None:
        """
        Sets the acceleration in nm/s^2
        :param acceleration:
        :return:
        """
        raise NotImplementedError()

    def getAcceleration(self) -> float:
        """
        Returns acceleration in nm/s^2
        :return:
        """
        raise NotImplementedError()

    def setDeceleration(self, deceleration: float) -> None:
        """
        Sets the deceleration in nm/s^2
        :param deceleration:
        :return:
        """
        raise NotImplementedError()

    def getDeceleration(self) -> float:
        """
        Returns deceleration in nm/s^2
        :return:
        """
        raise NotImplementedError()

    def getStoredPosition(self, isWvl: bool = True) -> float:
        """
        Returns stored motor position in steps or in nm.
        :param isWvl: returns store position in nm if True, else in steps
        :return: motor position in steps or in nm
        """
        raise NotImplementedError()

    def getOffset(self) -> float:
        """
        Returns difference between stored and current motor positions.
        :return:
        """
        raise NotImplementedError()

    def getPositionIs(self) -> float:
        """
        Returns current (not stored) motor position in steps.
        :return: current motor position in steps
        """
        raise NotImplementedError()

    def resetPositionIs(self) -> None:
        """
        Moves motor to position 0.
        :return: None
        """
        raise NotImplementedError()
    # ==================================================================================================================
    # Motor movement functions
    # ==================================================================================================================
    def goToWvl(self, wavelength: float, fast: bool) -> None:
        """
        Moves motor to the given wavelength in nm.
        :param wavelength: wavelength in nm
        :param fast: if True, moves motor with fast velocity, else with slow velocity
        :return: None
        """
        raise NotImplementedError()

    def startScan(self, wavelength: float, target: float) -> None:
        """
        Start scan from StartWvl to Target
        :param wavelength: start wavelength in nm
        :param target: target wavelength in nm
        :return: None
        """
        raise NotImplementedError()

    # ==================================================================================================================
    # Calibration functions#
    # ==================================================================================================================
    def Calibrate(self, wavelength: float) -> None:
        """
        Calibrates the system with wavelength
        :param wavelength: wavelength in nm
        :return:
        """
        raise NotImplementedError()

    # ==================================================================================================================
    # Auxiliary functions, which read or store variables in the code and on the EPOS board.
    # ==================================================================================================================
    def setStartWvl(self, wavelength: float) -> None:
        """
        Sets the start wavelength in nm. Auxiliary functions, which read or store variables in the code and on the
        EPOS board.
        :param wavelength: start wavelength in nm
        :return: None
        """
        raise NotImplementedError()

    def getStartWvl(self) -> float:
        """
        Returns start wavelength in nm. Auxiliary functions, which read or store variables in the code and on the
        EPOS board.
        :return: start wavelength in nm (float)
        """
        raise NotImplementedError()

    def setTargetWvl(self, wavelength: float) -> None:
        """
        Sets the target wavelength in nm. Auxiliary functions, which read or store variables in the code and on the
        EPOS board.
        :param wavelength:
        :return:
        """
        raise NotImplementedError()

    def getTargetWvl(self) -> float:
        """
        Returns target wavelength in nm. Auxiliary functions, which read or store variables in the code and on the
        EPOS board.
        :return: target wavelength in nm (float)
        """
        raise NotImplementedError()
