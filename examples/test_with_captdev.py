import logging
import sys
from multiprocessing import Value

from rich.logging import RichHandler
from PySide6.QtWidgets import QApplication

import CaptDeviceControl as captdev

sys.path.append('./src')
import LaserControl as Laser

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO,
    #                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s', )

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    conf_capt_dev = captdev.Config()
    #conf.load("config.yaml")

    start_capture_flag = Value('i', 0)
    capt_dev_model = captdev.Model(conf_capt_dev)
    capt_dev_controller = captdev.Controller(capt_dev_model, start_capture_flag)
    capt_dev_window = captdev.View(capt_dev_model, capt_dev_controller)
    capt_dev_window.show()

    conf = Laser.Config()
    model = Laser.Model(conf)
    controller = Laser.Controller(model, start_capture_flag)
    window = Laser.View(model, controller)

    controller.connect_capture_device(capt_dev_controller)

    window.show()


    sys.exit(app.exec())