import logging
import sys
import os
from pathlib import Path
from multiprocessing import Value, freeze_support

from rich.logging import RichHandler
from PySide6.QtWidgets import QApplication

import ADScopeControl as captdev

file_path, _ = os.path.split(os.path.realpath(__file__))
src_path = f"{file_path}/../src"
sys.path.append(src_path)

import SacherECLControl as Laser

if __name__ == "__main__":
    freeze_support()
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

    capt_conf = captdev.Config()
    capt_conf_file = Path('./CaptDeviceConfig.yaml')
    if capt_conf_file.exists(): 
        capt_conf.load(capt_conf_file, as_auto_save=True)
    capt_conf.autosave(enable=True, path='./')

    start_capture_flag = Value('i', 0)

    capt_dev_model = captdev.Model(capt_conf)
    capt_dev_controller = captdev.Controller(capt_dev_model, start_capture_flag)
    capt_dev_window = captdev.View(capt_dev_model, capt_dev_controller)


    conf = Laser.Config()
    conf_file = Path('./LaserConfig.yaml')
    if conf_file.exists():
        conf.load(conf_file, as_auto_save=True)
    conf.autosave(True, './')

    # Set the path to the EposCmd64.dll and the SacherMotorControl.pyd
    conf.epos_dll.set(Path(
        f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/EposCmd64.dll'))

    conf.motor_control_pyd.set(Path(
        f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/'
        f'lib/Python312/SacherMotorControl.pyd'))

    model = Laser.Model(conf)
    controller = Laser.Controller(model, start_capture_flag)
    window = Laser.View(model, controller)
    capt_dev_window.show()

    controller.supervise(capt_dev_controller)

    window.show()


    sys.exit(app.exec())