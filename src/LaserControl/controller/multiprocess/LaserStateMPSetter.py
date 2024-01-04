class LaserState:
    def __init__(self):
        # Multiprocessing Information
        self._pid = None
        self._ppid = None

        self._wavelength = 0
        self._min_wavelength = 0
        self._max_wavelength = 0
        self._velocity = 0
        self._acceleration = 0
        self._deceleration = 0

    def reinit(self, fields: dict):
        for k, v in fields.items():
            setattr(self, k, v)

    # =========== Multiprocessing Information
    @property
    def pid(self):
        return self._pid

    @property
    def ppid(self):
        return self._ppid

    # =========== Laser Information
    @property
    def wavelength(self):
        return self._wavelength

    @property
    def min_wavelength(self):
        return self._min_wavelength

    @property
    def max_wavelength(self):
        return self._max_wavelength

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @property
    def deceleration(self):
        return self._deceleration


class LaserStateMPSetter(LaserState):

    def __init__(self, state_queue):
        super().__init__()
        self._state_queue = state_queue

    @LaserState.pid.setter
    def pid(self, value):
        self._pid = value
        self._state_queue.put(self.to_simple_class())

    @LaserState.ppid.setter
    def ppid(self, value):
        self._ppid = value
        self._state_queue.put(self.to_simple_class())


    @LaserState.wavelength.setter
    def wavelength(self, value):
        self._wavelength = value
        self._state_queue.put(self.to_simple_class())

    @LaserState.min_wavelength.setter
    def min_wavelength(self, value):
        self._min_wavelength = value
        self._state_queue.put(self.to_simple_class())

    @LaserState.max_wavelength.setter
    def max_wavelength(self, value):
        self._max_wavelength = value
        self._state_queue.put(self.to_simple_class())

    @LaserState.velocity.setter
    def velocity(self, value):
        self._velocity = value
        self._state_queue.put(self.to_simple_class())

    @LaserState.acceleration.setter
    def acceleration(self, value):
        self._acceleration = value
        self._state_queue.put(self.to_simple_class())

    @LaserState.deceleration.setter
    def deceleration(self, value):
        self._deceleration = value
        self._state_queue.put(self.to_simple_class())

    def to_simple_class(self) -> LaserState:
        exclude = ["_state_queue"]
        laserstate = LaserState()
        to_dict = {}
        for item, value in self.__dict__.items():
            if item in exclude:
                continue
            else:
                to_dict[item] = value
        laserstate.reinit(to_dict)
        return laserstate