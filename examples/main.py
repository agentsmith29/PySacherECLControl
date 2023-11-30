import logging
import sys
from PySide6.QtWidgets import QApplication

sys.path.append('./src')
import LaserControl as Laser

if __name__ == "__main__":

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    conf = Laser.Config()
    #conf.load("config.yaml")

    model = Laser.Model(conf)
    controller = Laser.Controller(model)
    window = Laser.View(model, controller)


    window.show()


    sys.exit(app.exec())