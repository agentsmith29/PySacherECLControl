import logging
import os
import pathlib
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication
from rich.logging import RichHandler

sys.path.append('../src')
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

    conf = Laser.Config()
    conf_file = Path('./LaserConfig.yaml')
    if conf_file.exists():
        conf.load(conf_file, as_auto_save=True)
    conf.autosave(True, './')
    
    #conf.save()
    #conf.load('./LaserConfig.yaml', as_auto_save=True)

    # Set the path to the EposCmd64.dll and the SacherMotorControl.pyd
    conf.epos_dll.set(pathlib.Path(
        f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/EposCmd64.dll'))

    conf.motor_control_pyd.set(pathlib.Path(
        f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/'
        f'lib/Python312/SacherMotorControl.pyd'))



    conf.module_log_level = logging.DEBUG
    conf.module_log_enabled = True

    model = Laser.Model(conf)
    controller = Laser.Controller(model, None)
    controller.internal_log_level = logging.DEBUG
    controller.internal_log_enabled = True
    window = Laser.View(model, controller)

    #controller.start_wavelength_sweep.emit(
    #    model.sweep_start_wavelength,
    #    model.sweep_stop_wavelength,
    #)

    window.show()

    sys.exit(app.exec())
