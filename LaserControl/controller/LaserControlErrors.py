class LaserNotConnectedError(Exception):
    pass

    def __init__(self, message="Fails to open USB! Please check if USB is connected."):
        self.message = message
        super().__init__(self.message)
