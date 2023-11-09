import logging
import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QDoubleSpinBox, \
    QGridLayout, QWidget, QGroupBox

from LaserControl.controller.LaserControlController import LaserControlController
from LaserControl.view.Ui_LaserControlWindow import Ui_LaserControlWindow
from LaserControl.model.LaserControlModel import LaserControlModel
from view.WidgetLaserInformation import WidgetLaserInformation


class LaserControlView(QMainWindow):

    def __init__(self, model: LaserControlModel, controller: LaserControlController):
        super().__init__()
        self.logger = logging.getLogger("LaserControlWindow")

        self._ui = Ui_LaserControlWindow()

        self._ui.setupUi(self)

        self.model: LaserControlModel = model
        self.controller = controller

        self.model.laser_config.velocity.view.add_new_view(self._ui.sb_velocity)
        self.model.laser_config.acceleration.view.add_new_view(self._ui.sb_acc)
        self.model.laser_config.deceleration.view.add_new_view(self._ui.sb_dec)
        self.model.laser_config.wl_sweep_start.view.add_new_view(self._ui.sb_sweep_start)
        self.model.laser_config.wl_sweep_stop.view.add_new_view(self._ui.sb_sweep_stop)

        # Laser Information
        self.laser_information = WidgetLaserInformation()
        self._ui.grd_system_info.addWidget(self.laser_information, 0, 0, 1, 1)


        self._connect_controls()
        self._connect_signals()

    def _on_uncertainty_changed(self, uncertainty):
        self.uncertainty_dist_plot.uncertainty = uncertainty

    def _connect_controls(self):
        # USB Connection List
        self._ui.cb_port_selection.addItems(self.model.laser_config.available_ports.get())
        self._ui.cb_port_selection.currentTextChanged.connect(self._on_port_changed)

        # Buttons
        self._ui.btn_connect.clicked.connect(self._on_btn_connect_clicked)
        self._ui.btn_move_to_wavelength.clicked.connect(self._on_btn_move_to_wavelength_clicked)
        # Spinboxes

        self.model.port = self._ui.cb_port_selection.currentText()

        # Sweep start
        self._ui.btn_start_sweep.clicked.connect(self._on_btn_start_sweep_clicked)

        # Connect the Spinboxes for the sweep settings. A change in values sets the new sweep settings
        self._ui.sb_sweep_start.valueChanged.connect(self._on_sb_sweep_start_changed)
        self._ui.sb_sweep_stop.valueChanged.connect(self._on_sb_sweep_stop_changed)

    def _connect_signals(self):

        # Triggerd if the laser connection status changes
        self.model.signals.connected_changed.connect(self._on_laser_connected_changed)
        self.model.signals.laser_is_moving_changed.connect(self._on_laser_is_moving_changed)

        #self.uncertainty_model.signals.uncertainty_changed.connect(self._on_uncertainty_changed)

        # Triggerd if the laser port changes
        self.model.signals.current_wavelength_changed.connect(self._on_wavelength_changed)

        self.model.signals.velocity_changed.connect(self._on_velocity_changed)
        self.model.signals.acceleration_changed.connect(self._on_acceleration_changed)
        self.model.signals.deceleration_changed.connect(self._on_deceleration_changed)

        # Sweep Settings
        self.model.signals.sweep_start_wavelength_changed.connect(self._on_sweep_start_changed)
        self.model.signals.sweep_stop_wavelength_changed.connect(self._on_sweep_stop_changed)

        # ==================================================================================================================
        # Slots that are triggerd if the laser connection changes
        # ==================================================================================================================

    def _on_laser_connected_changed(self, connected):
        if connected:
            self._ui.btn_connect.setText("Disconnect")
            self.laser_information.set_connection_state(True, f"Connected ({self.model.port})")
        else:
            self._ui.btn_connect.setText("Connect")
            self.laser_information.set_connection_state(False)

    def _on_laser_is_moving_changed(self, is_moving):
        self._ui.btn_move_to_wavelength.setEnabled(not is_moving)
        self._ui.btn_start_sweep.setEnabled(not is_moving)
        self.laser_information.set_movement_state(is_moving)

    def _on_wavelength_changed(self, wavelength):
        # self.logger.debug(f"Wavelength changed to: {wavelength}. "
        #                  f"Range ({self.model.min_laser_wavelength}-{self.model.max_laser_wavelength})nm")

        self._ui.lbl_min_wavelength.setText(str(self.model.min_laser_wavelength))
        self._ui.lbl_max_wavelength.setText(str(self.model.max_laser_wavelength))

        self._ui.slider_wavelength.setMinimum(self.model.min_laser_wavelength)
        self._ui.slider_wavelength.setMaximum(self.model.max_laser_wavelength)

        self._ui.sb_set_wavelength.setMinimum(self.model.min_laser_wavelength)
        self._ui.sb_set_wavelength.setMaximum(self.model.max_laser_wavelength)

        # Set the minimum and maximum values for the sweep start and stop
        self._ui.sb_set_wavelength.setValue(wavelength)
        self._ui.lcd_wavelength.display(wavelength)
        self._ui.slider_wavelength.setValue(wavelength)

    def _on_velocity_changed(self, velocity: float):
        self.logger.debug(f"Velocity changed to: {velocity} "
                          f"[{self.model.min_velocity}, {self.model.max_velocity}]")

        self._ui.sb_velocity.setMinimum(self.model.min_velocity)
        self._ui.sb_velocity.setMaximum(self.model.max_velocity)
        self._ui.sb_velocity.setValue(velocity)

    def _on_deceleration_changed(self, deceleration: float):
        self.logger.debug(f"Deceleration changed to: {deceleration} "
                          f"[{self.model.min_deceleration}, {self.model.max_deceleration}]")

        self._ui.sb_dec.setMinimum(self.model.min_deceleration)
        self._ui.sb_dec.setMaximum(self.model.max_deceleration)
        self._ui.sb_dec.setValue(deceleration)

    def _on_acceleration_changed(self, acceleration: float):
        self.logger.debug(f"Acceleration changed to: {acceleration} "
                          f"[{self.model.min_acceleration}, {self.model.max_acceleration}]")

        self._ui.sb_acc.setMinimum(self.model.min_acceleration)
        self._ui.sb_acc.setMaximum(self.model.max_acceleration)
        self._ui.sb_acc.setValue(acceleration)

    def _on_sweep_start_changed(self, sweep_start):
        self._ui.sb_sweep_start.setRange(self.model.min_laser_wavelength, self.model.max_laser_wavelength)
        self._ui.sb_sweep_start.setValue(sweep_start)

    def _on_sweep_stop_changed(self, sweep_stop):
        self._ui.sb_sweep_stop.setRange(self.model.min_laser_wavelength, self.model.max_laser_wavelength)
        self._ui.sb_sweep_stop.setValue(sweep_stop)

        # ==================================================================================================================
        # Slots that are triggerd if the user changes something
        # ==================================================================================================================

    def _on_port_changed(self, port_string):
        self.model.port = port_string
        self.model.laser_config.port.set(port_string)
        self.logger.debug(f"Port changed to: {port_string}")
        # self._ui.cb_port_selection.setText(port_string)

    def _on_btn_connect_clicked(self):
        if self.model.connected:
            self.logger.debug("Attempting to disconnect from laser")
            self.controller.read_laser_settings()
        elif not self.model.connected:
            self.logger.debug(f"Attempting to connect to laser on port: {self.model.port}")
            self.controller.read_laser_settings()

    def _on_btn_move_to_wavelength_clicked(self):
        self.logger.debug(f"Attempting to set wavelength to: {self._ui.sb_set_wavelength.value()}")
        self.controller._move_to_wavelength(self._ui.sb_set_wavelength.value(), False)

    def _on_sb_sweep_start_changed(self, value):
        try:
            self.logger.debug(f"Sweep start changed. New Range {value}-{self.model.sweep_stop_wavelength}")
            self.model.sweep_start_wavelength = value
        except Exception as e:
            self.logger.error(e)
            self.model.sweep_stop_wavelength = value

    def _on_sb_sweep_stop_changed(self, value):
        try:
            self.logger.debug(f"Sweep stop changed. New Range {self.model.sweep_start_wavelength}-{value}")
            self.model.sweep_stop_wavelength = value
        except Exception as e:
            self.logger.error(e)
            self.model.sweep_start_wavelength = value
        # self.controller.set_sweep_wavelength_range(self._ui.sb_sweep_start.value(), self._ui.sb_sweep_stop.value())

    def _on_btn_start_sweep_clicked(self):
        self.logger.warning("Sweep manually started")
        self.controller.start_wavelength_sweep(self.model.sweep_start_wavelength, self.model.sweep_stop_wavelength)