import logging
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
    #conf.load('./LaserConfig.yaml', as_auto_save=True)
    conf.autosave(True, './LaserConfig.yaml')
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