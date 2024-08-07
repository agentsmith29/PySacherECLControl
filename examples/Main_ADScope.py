import logging
import sys
import os
from multiprocessing import Value

from rich.logging import RichHandler
from PySide6.QtWidgets import QApplication

import ADScopeControl as captdev

file_path, _ = os.path.split(os.path.realpath(__file__))
src_path = f"{file_path}/../src"
print("src_path:", src_path)
sys.path.append(src_path)

import SacherECLControl as Laser

if __name__ == "__main__":
    FORMAT = "%(name)s %(message)s"
    logging.basicConfig(
        level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
            RichHandler(rich_tracebacks=True)
        ]
    )

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    conf_capt_dev = captdev.Config()
    #conf_capt_dev.load("CaptDeviceConfig.yaml")
    conf_capt_dev.autosave()

    start_capture_flag = Value('i', 0)

    capt_dev_model = captdev.Model(conf_capt_dev)
    capt_dev_controller = captdev.Controller(capt_dev_model, start_capture_flag)
    capt_dev_window = captdev.View(capt_dev_model, capt_dev_controller)


    conf = Laser.Config()
    model = Laser.Model(conf)
    controller = Laser.Controller(model, start_capture_flag)
    window = Laser.View(model, controller)
    capt_dev_window.show()

    controller.connect_capture_device(capt_dev_controller)

    window.show()


    sys.exit(app.exec())