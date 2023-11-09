from ctypes import c_int, c_byte


class LaserState:
    def __init__(self):
        # Multiprocessing Information
        self._pid = None

        self._port: str = "None"

        self._connected: bool = False

    def reinit(self, fields: dict):
        for k, v in fields.items():
            setattr(self, k, v)

    # =========== Multiprocessing Information
    @property
    def pid(self):
        return self._pid

    # =========== WaveForms Runtime (DWF) Information
    @property
    def port(self):
        return self._port

    # Connection state
    @property
    def connected(self):
        return self._connected



class LaserStateMPSetter(LaserState):

    def __init__(self, state_queue):
        super().__init__()
        self._state_queue = state_queue

    # =========== Multiprocessing Information
    @LaserState.pid.setter
    def pid(self, value):
        self._pid = value
        self._state_queue.put(self.to_simple_class())

    # =========== WaveForms Runtime (DWF) Information
    @LaserState.port.setter
    def port(self, value):

        self._port = value
        self._state_queue.put(self.to_simple_class())

    # =========== Connection State
    @LaserState.connected.setter
    def connected(self, value):
        self._connected = value
        self._state_queue.put(self.to_simple_class())



    def to_simple_class(self) -> LaserState:
        exclude = ["_state_queue"]
        ad2state = LaserState()
        to_dict = {}
        for item, value in self.__dict__.items():
            if item in exclude:
                continue
            else:
                to_dict[item] = value
        ad2state.reinit(to_dict)
        return ad2state
