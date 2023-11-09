from multiprocessing import Value, Array

from controller.multiprocess.LaserStateArray import LaserStateArray
from controller.multiprocess.logging import log_info
from controller.multiprocess.move_to_wavelength import move_to_wavelength


def wavelength_sweep(laser_port, current_wavelength: Value,
                        laser_connected_flag: Value,  # Flag if the laser is connected
                        laser_moving_flag: Value,  # Flag if the laser is moving
                        laser_at_start_position_flag: Value,  # Flag if the laser is at the starting position
                        laser_at_end_position_flag: Value,  # Flag if the laser is at the end position
                        capt_device_started_flag: Value,  # Flag if the capture device is started
                        laser_finished_flag: Value,  # Flag if the laser is finished
                        start_wavelength: int, end_wavelength: int,
                        laser_state: Value):

    laser_finished_flag.value = False
    #laser_state.value.connected = False
    log_info(f"Starting sweep from {start_wavelength} to {end_wavelength}.")
    log_info(f"Resetting laser to start wavelength {start_wavelength}")
    move_to_wavelength(
        laser_port=laser_port,
        current_wavelength=current_wavelength,
        laser_connected_flag=laser_connected_flag,
        laser_moving_flag=laser_moving_flag,
        laser_finished_flag=laser_at_start_position_flag,
        wavelength=start_wavelength,
        vel_fast=True,
        capture_device_started_flag=None)

    log_info(f"Starting sweep from {start_wavelength} to {end_wavelength}.")
    move_to_wavelength(
        laser_port=laser_port,
        current_wavelength=current_wavelength,
        laser_connected_flag=laser_connected_flag,
        laser_moving_flag=laser_moving_flag,
        laser_finished_flag=laser_at_end_position_flag,
        wavelength=end_wavelength,
        vel_fast=False,
        capture_device_started_flag=capt_device_started_flag)

    log_info(f"Finished sweep from {start_wavelength} to {end_wavelength}.")
    #laser_state.connected = False
