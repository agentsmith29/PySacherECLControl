import logging
import sys

from PySide6.QtWidgets import QApplication

import Laser
from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
from generics.logger import setup_logging

if __name__ == "__main__":
    app = QApplication()
    setup_logging()

    logging.warning("[TEST] LaserControlWindow.py is not meant to be run as a script.")

    vaut_config = VAutomatorConfig.load_config("../configs/init_config.yaml")

    laser_model = Laser.Model()
    laser_controller = Laser.Controller(laser_model, vaut_config.laser_config)
    laser_window = Laser.ControlWindow(laser_model, laser_controller)
    # test_win = StructureSelector()

    laser_window.show()
    sys.exit(app.exec())