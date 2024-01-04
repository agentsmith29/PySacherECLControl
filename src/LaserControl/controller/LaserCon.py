import io
import logging
import os
import sys
import tempfile
from contextlib import contextmanager

from rich.logging import RichHandler

from LaserControl.controller.ErrorConverter import ErrorConverter

if os.getenv("LASER_SIM") == "TRUE":
    from LaserControl.libs.LaserLibSimulator import LaserLibSimulator as LaserLib
else:
    try:
        from LaserControl.libs import laserSacher as LaserLib
    except Exception as e:
        from LaserControl.libs.LaserLibSimulator import LaserLibSimulator as LaserLib


@contextmanager
def stdout_redirector(stream):
    # The original fd stdout points to. Usually 1 on POSIX systems.
    original_stdout_fd = sys.stdout.fileno()

    def _redirect_stdout(to_fd ):
        """Redirect stdout to the given file descriptor."""
        # Flush the C-level buffer stdout
        sys.stdout.flush()
        # libc.fflush(c_stdout)
        # Flush and close sys.stdout - also closes the file descriptor (fd)
        sys.stdout.close()
        # Make original_stdout_fd point to the same file as to_fd
        os.dup2(to_fd, original_stdout_fd)
        # Create a new sys.stdout that points to the redirected fd
        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

    # Save a copy of the original stdout fd in saved_stdout_fd
    saved_stdout_fd = os.dup(original_stdout_fd)
    try:
        # Create a temporary file and redirect stdout to it
        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stdout(tfile.fileno())
        # Yield to caller, then redirect stdout back to the saved fd
        yield
        _redirect_stdout(saved_stdout_fd)
        # Copy contents of temporary file to the given stream
        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        redir = tfile.read().decode("utf-8")
        #print(redir)
        redirtext_stripped = ErrorConverter.convert(redir)
        stream.write(redirtext_stripped)
    finally:
        tfile.close()
        os.close(saved_stdout_fd)
        # os.dup2(saved_stdout_fd, sys.stdout.fileno())
        # sys.stdout = original

class LaserCon(object):

    def __init__(self, port=0):
        self.handler = RichHandler(rich_tracebacks=True)
        self.logger = logging.getLogger(f"AD2Controller({os.getpid()})")
        self.logger.handlers = [self.handler]
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s %(message)s')
        self.handler.setFormatter(formatter)
        #self.logger.addHandler(logging.StreamHandler())
        #self.logger.setLevel(logging.DEBUG)
        self.laser_con = LaserLib()
        self._connected = False
        self._connect_to_laser(self.laser_con, port)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.laser_con.closeMotorConnection()
        self.logger.info("Laser Connection Closed")
        self._connected = False

    def _connect_to_laser(self, laser_conn, laser_port):
        self.logger.info(f"Connection to Laser on Port {laser_port}.")
        f = io.StringIO()
        # with stdout_redirector(f):
        #     laser_conn.connectMotor(f"{laser_port}")
        self._connected = True
        return self._connected

    @property
    def connected(self) -> bool:
        """ Wrapper for the C Function call """
        return bool(self._connected)

    @property
    def current_wavelength(self) -> float:
        """ Wrapper for the C Function call """
        return float(self.laser_con.getCurrentWavelength())

    @property
    def deceleration(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laser_con.getDeceleration())

    @deceleration.setter
    def deceleration(self, value: float) -> None:
        ''' Wrapper for the C Function call '''
        self.laser_con.setDeceleration(value)

    @property
    def acceleration(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laser_con.getAcceleration())

    @acceleration.setter
    def acceleration(self, value: float) -> None:
        ''' Wrapper for the C Function call '''
        self.laser_con.setAcceleration(value)

    @property
    def velocity(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laser_con.getVelocity())

    @velocity.setter
    def velocity(self, value: float) -> None:
        ''' Wrapper for the C Function call '''
        self.laser_con.setVelocity(value)

    @property
    def min_wavelength(self) -> float:
        return float(830)

    @property
    def max_wavelength(self) -> float:
        return float(880)

    def go_to_wvl(self, wavelength: float, vel_type: bool) -> None:
        self.laser_con.goToWvl(wavelength, vel_type)




