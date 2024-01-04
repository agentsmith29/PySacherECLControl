import io
import time
from multiprocessing import Value

from LaserControl.controller.LaserCon import LaserCon


#from LaserControl.controller.multiprocess.logging import log_debug, log_info


def move_to_wavelength(laser_port, current_wavelength: Value,
                          laser_connected_flag: Value,
                          laser_moving_flag: Value,
                          laser_finished_flag: Value,
                          wavelength: int, vel_fast=False,
                          capture_device_started_flag: Value = None):
    laser_moving_flag.value = False

    with LaserCon(laser_port.value) as con:
        current_wavelength.value = con.current_wavelength
        laser_connected_flag.value = con.connected
        log_debug(f"Current Wavelength: {current_wavelength.value}")

        # Move the laser to the new wavelength
        f = io.StringIO()

        time_start = 0
        # with stdout_redirector(f) as s:
        log_info(f"Go to selected wavelength. Started moving laser to {wavelength}.")
        laser_finished_flag.value = False
        laser_moving_flag.value = True
        if capture_device_started_flag is not None:
            capture_device_started_flag.value = True
        time_start = time.time()
        con.go_to_wvl(wavelength, vel_fast)
        time_end = time.time()
        if capture_device_started_flag is not None:
            capture_device_started_flag.value = False
        laser_finished_flag.value = True
        laser_moving_flag.value = False
        log_info(f"Go to selected wavelength finished.")

        current_wavelength.value = con.current_wavelength
        log_info(f"Current Wavelength: {current_wavelength.value}. Took {time_end - time_start} seconds to move.")
        time.sleep(1)  # Wait for stabilizing
    laser_connected_flag.value = False  # We need to manually set this