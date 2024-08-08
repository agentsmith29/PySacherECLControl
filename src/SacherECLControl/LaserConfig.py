import logging
import os
from pathlib import Path

import confPy6 as cfg


class LaserConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()

        # Set the path to the EposCmd64.dll
        self.epos_dll = cfg.Field(Path("./EposCmd64.dll"))
        # Set the path to the SacherMotorControl.pyd
        self.motor_control_pyd = cfg.Field(
            Path(f"./SacherMotorControl.pyd"),
            env_var="MOTOR_CONTROL_PYD")

        self.wl_sweep_start = cfg.Field(857)
        self.wl_sweep_stop = cfg.Field(870)
        self.velocity = cfg.Field(2.0)
        self.acceleration = cfg.Field(1.0)
        self.deceleration = cfg.Field(1.0)
        self.available_ports = cfg.Field(['USB0', 'USB1', 'USB2', 'USB3', 'USB4', 'USB5', 'USB6', 'USB7', 'USB8', 'USB9'])
        self.port = cfg.Field("USB0")

        self.register()
