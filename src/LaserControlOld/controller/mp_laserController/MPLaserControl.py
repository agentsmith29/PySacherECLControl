import os
import sys
import tempfile
import time
from contextlib import contextmanager
from ctypes import c_int, byref, c_double, cdll, create_string_buffer, c_int32
from multiprocessing import Queue, Value
import io

from AD2CaptDevice.controller.mp_AD2Capture.AD2StateMPSetter import AD2StateMPSetter
from Laser.LaserControl.controller.BaseLaserController import LaserNotConnectedError
from Laser.LaserControl.controller.mp_laserController.LaserStateMPSetter import LaserStateMPSetter
from constants.dwfconstants import acqmodeRecord, DwfStateConfig, DwfStatePrefill, DwfStateArmed, enumfilterType, \
    enumfilterUSB, enumfilterDemo


from libs.LaserLib import laserSacher as LaserLib


class LLIBErrorConvert:

    @staticmethod
    def convert(msg, additional_message=""):

        msg = msg.replace('>>>>>>>>>>>>>>>>>>>>  ', '').strip()

        if "Fails to open" in msg and "Please check if USB is connected" in msg:
            if additional_message is not None or additional_message != "":
                raise LaserNotConnectedError(f"{msg}. {additional_message}")
            else:
                raise LaserNotConnectedError(f"{msg}")
        else:
            return msg


def _mp_log_debug(msg, prefix="LAS Thread"):
    print(f"DBG  | [{prefix}/{os.getpid()}]: {msg}")


def _mp_log_error(msg, prefix="LAS Thread"):
    print(f"ERR  | [{prefix}/{os.getpid()}]: {msg}")


def _mp_log_info(msg, prefix="LAS Thread"):
    print(f"INF  | [{prefix}/{os.getpid()}]: {msg}")


def _mp_log_warning(msg, prefix="LAS Thread"):
    print(f"WARN | [{prefix}/{os.getpid()}]: {msg}")





# def mp_start_laser_control(laser_state_queue: Queue, laser_moving, port="USB0"):
#    laser_state = LaserStateMPSetter(laser_state_queue)
#    laser_state.port = port
#    laser_conn = laserSacher()
#    return laser_conn

class LaserConnection(object):
    @property
    def current_wavelength(self) -> float:
        """ Wrapper for the C Function call """
        return float(self.laser_con.getCurrentWavelength())

    @property
    def deceleration(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laser_con.getDeceleration() / (-1.986))

    @property
    def acceleration(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laser_con.getAcceleration() / (-1.986))

    @property
    def velocity(self) -> float:
        ''' Wrapper for the C Function call '''
        return float(self.laser_con.getVelocity() / (-1.986))

    @property
    def min_wavelength(self) -> float:
        return float(830)

    @property
    def max_wavelength(self) -> float:
        return float(880)

    def go_to_wvl(self, wavelength: float, vel_type: bool) -> None:
        self.laser_con.goToWvl(wavelength, vel_type)

    def __init__(self, port=0):
        self.laser_con = LaserLib()
        self._connected = False
        self.connected = _connect_to_laser(self.laser_con, port)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.laser_con.closeMotorConnection()
        _mp_log_info("Laser Connection Closed")
        self.connected = False





def init_laser_connection():
    pass

def _move_to_wavelength():
    pass

def mp_wavelength_sweep(laser_port, current_wavelength: Value,
                        laser_connected_flag: Value,            # Flag if the laser is connected
                        laser_moving_flag: Value,               # Flag if the laser is moving
                        laser_at_start_position_flag: Value,    # Flag if the laser is at the starting position
                        laser_at_end_position_flag: Value,      # Flag if the laser is at the end position
                        capt_device_started_flag: Value,        # Flag if the capture device is started
                        laser_finished_flag: Value,             # Flag if the laser is finished
                        start_wavelength: int, end_wavelength: int):
    laser_finished_flag.value = False
    _mp_log_info(f"Starting sweep from {start_wavelength} to {end_wavelength}.")
    _mp_log_info(f"Resetting laser to start wavelength {start_wavelength}")
    mp_move_to_wavelength(
        laser_port=laser_port,
        current_wavelength=current_wavelength,
        laser_connected_flag=laser_connected_flag,
        laser_moving_flag=laser_moving_flag,
        laser_finished_flag=laser_at_start_position_flag,
        wavelength=start_wavelength,
        vel_fast=True,
        capture_device_started_flag=None)

    _mp_log_info(f"Starting sweep from {start_wavelength} to {end_wavelength}.")
    mp_move_to_wavelength(
        laser_port=laser_port,
        current_wavelength=current_wavelength,
        laser_connected_flag=laser_connected_flag,
        laser_moving_flag=laser_moving_flag,
        laser_finished_flag=laser_at_end_position_flag,
        wavelength=end_wavelength,
        vel_fast=False,
        capture_device_started_flag=capt_device_started_flag)

    _mp_log_info(f"Finished sweep from {start_wavelength} to {end_wavelength}.")
    laser_finished_flag.value = True

def mp_move_to_wavelength(laser_port, current_wavelength: Value,
                          laser_connected_flag: Value,
                          laser_moving_flag: Value,
                          laser_finished_flag: Value,
                          wavelength: int, vel_fast=False,
                          capture_device_started_flag: Value = None):
    laser_moving_flag.value = False

    with LaserConnection(laser_port.value) as laser_conn:
        current_wavelength.value = laser_conn.current_wavelength
        laser_connected_flag.value = laser_conn.connected
        _mp_log_debug(f"Current Wavelength: {current_wavelength.value}")

        # Move the laser to the new wavelength
        f = io.StringIO()

        time_start = 0
        #with stdout_redirector(f) as s:
        _mp_log_info(f"Go to selected wavelength. Started moving laser to {wavelength}.")
        laser_finished_flag.value = False
        laser_moving_flag.value = True
        if capture_device_started_flag is not None:
            capture_device_started_flag.value = True
        time_start = time.time()
        laser_conn.go_to_wvl(wavelength, vel_fast) 
        time_end = time.time()
        if capture_device_started_flag is not None:
            capture_device_started_flag.value = False
        laser_finished_flag.value = True
        laser_moving_flag.value = False
        _mp_log_info(f"Go to selected wavelength finihsed.")
           

        current_wavelength.value = laser_conn.current_wavelength
        _mp_log_info(f"Current Wavelength: {current_wavelength.value}. Took {time_end - time_start} seconds to move.")
        time.sleep(1) # Wait for stabilizing        
    laser_connected_flag.value = False # We need to manually set this



def _disconnect_from_laser(laser_conn):
    _mp_log_info(f"Disconnecting Laser.")
    f = io.StringIO()
    with stdout_redirector(f):
        laser_conn.closeMotorConnection()
    return False

def _connect_to_laser(laser_conn, laser_port):
    _mp_log_info(f"Connection to Laser on Port USB{laser_port}.")
    f = io.StringIO()
    with stdout_redirector(f):
        laser_conn.connectMotor(f"USB{laser_port}")
    return True
