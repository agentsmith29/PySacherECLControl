import logging
import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QDoubleSpinBox, \
    QGridLayout, QWidget, QGroupBox


from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
# import Laser
import Laser.LaserUncertainty as LaserUncertainty
from Laser.LaserControl.controller.BaseLaserController import BaseLaserController
from Laser.LaserControl.model.LaserModel import LaserModel
# Import the UI design
from Laser.LaserControl.view.Ui_LaserControlWindow import Ui_LaserControlWindow

from Laser.LaserControl.view.WidgetLaserInformation import WidgetLaserInformation
from mcpy.userinterface.UncertaintyWidget import UncertaintyWidget


class LaserControlWindow(QMainWindow):

    def __init__(self, model: LaserModel, controller: BaseLaserController):

        super().__init__()
        self.logger = logging.getLogger("LaserControlWindow")

        self.controller = controller
        self.model: LaserModel = model


        self._ui = Ui_LaserControlWindow()
        self._ui.setupUi(self)

        # Disable all Controls until the Laser is connected
        self._ui.group_wavelength_settings.setEnabled(True)
        # self._ui.group_sweep_settings.setEnabled(False)
        self._ui.group_motor_profile.setEnabled(True)

        # Add WidgetCapturingInformation to the layout
        self.laser_information = WidgetLaserInformation()
        self._ui.grd_system_info.addWidget(self.laser_information, 0, 0, 1, 1)

        self.uncertainty_model = LaserUncertainty.Model()
        self.uncertainty_view = LaserUncertainty.View(self.uncertainty_model)
        self.uncertainty_controller = LaserUncertainty.Controller(self.uncertainty_model, self.uncertainty_view)
        self._ui.grd_uncertainty.addWidget(self.uncertainty_view, 0, 0, 1, 1)

        # Add the Uncertainty Table
        self.uncertainty_dist_plot = UncertaintyWidget()
        self._ui.grd_uncertainty_dist.addWidget(self.uncertainty_dist_plot)

        self._ui.cb_port_selection.addItems(self.controller.port_list)
        self._ui.table_laser_control.setCurrentIndex(0)



        # Set the ranges for the Spinboxes
        self._ui.sb_sweep_start.setRange(self.model.min_laser_wavelength, self.model.max_laser_wavelength)
        self._ui.sb_sweep_start.setValue(self.model.sweep_start_wavelength)
        self._ui.sb_sweep_stop.setRange(self.model.min_laser_wavelength, self.model.max_laser_wavelength)
        self._ui.sb_sweep_stop.setValue(self.model.sweep_stop_wavelength)

        self._connect_controls()
        self._connect_signals()

        self.controller.read_laser_settings()

        #self.controller.read_laser_settings()

    def _on_uncertainty_changed(self, uncertainty):
        self.uncertainty_dist_plot.uncertainty = uncertainty

    def _connect_controls(self):
        # Buttons
        self._ui.btn_connect.clicked.connect(self._on_btn_connect_clicked)
        self._ui.btn_move_to_wavelength.clicked.connect(self._on_btn_move_to_wavelength_clicked)
        # Spinboxes
        self._ui.cb_port_selection.currentTextChanged.connect(self._on_port_changed)
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

        self.uncertainty_model.signals.uncertainty_changed.connect(self._on_uncertainty_changed)

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
            #self._ui.group_wavelength_settings.setEnabled(True)
            #self._ui.group_sweep_settings.setEnabled(True)
            #self._ui.group_motor_profile.setEnabled(True)
            self._ui.btn_connect.setText("Disconnect")
            self.laser_information.set_connection_state(True, f"Connected ({self.model.port})")
        else:
            # Disable all Controls until the Laser is connected
            #self._ui.group_wavelength_settings.setEnabled(False)
            #self._ui.group_sweep_settings.setEnabled(False)
            #self._ui.group_motor_profile.setEnabled(False)
            self._ui.btn_connect.setText("Connect")
            self.laser_information.set_connection_state(False)

    def _on_laser_is_moving_changed(self, is_moving):
        self._ui.btn_move_to_wavelength.setEnabled(not is_moving)
        self._ui.btn_start_sweep.setEnabled(not is_moving)
        self.laser_information.set_movement_state(is_moving)

    def _on_wavelength_changed(self, wavelength):
        #self.logger.debug(f"Wavelength changed to: {wavelength}. "
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
        self.logger.debug(f"Port changed to: {port_string}")
        # self._ui.cb_port_selection.setText(port_string)

    def _on_btn_connect_clicked(self):

        if self.model.connected:
            self.logger.debug("Attempting to disconnect from laser")
            self.controller.disconnect()
        elif not self.model.connected:
            self.logger.debug("Attempting to connect to laser on port: {self.model.port}")
            self.controller.connect_device(self.model.port)

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
        self.logger.Warning("Sweep manually started")
        self.controller.start_wavelength_sweep(self.model.sweep_start_wavelength, self.model.sweep_stop_wavelength)


# class LaserControlWidget(QWidget):
#     def __init__(self, laser_controller: BaseLaserController, laser_model: LaserModel):
#         super().__init__()
#
#         self.laser_controller = laser_controller
#         self.laser_model = laser_model
#
#         self.logger = logging.getLogger("LaserControlWidget")
#
#         self.layout = QGridLayout()
#         self.setLayout(self.layout)
#         self.init_UI()
#
#         # self.laser.signals.connected_changed.connect()
#         # self.laser.signals.port_changed.connect(lambda s: self.edit_set_usb.setText(s))
#         # self.laser.signals.current_speed_settings.connect(self.update_speed_param)
#         # self.laser.signals.current_wavelength.connect(self.update_wavelength_param)
#
#     # def init_UI(self):
#     #     # # Add a QLineEdit with a button for training folder location
#     #     self.edit_set_usb = QLineEdit()
#     #     self.edit_set_usb.setText("USB 1")
#     #     self.layout.addWidget(self.edit_set_usb, 0, 0, 1, 3)
#     #
#     #
#     #
#     #     #self.laser_uncertainty = WidgetLaserUncertaintyView()
#     #     #self.layout.addWidget(self.laser_uncertainty, 1, 1, 1, 1)
#     #     #self.laser_uncertainty.btn_load_cal_data.clicked.connect(self._load_cal_data)
#     #
#     #
#     #     self.load_cal_data = QPushButton()
#     #     self.load_cal_data.clicked.connect(self._load_cal_data)
#     #     self.layout.addWidget(self.laser_uncertainty, 1, 1, 1, 1)
#     #
#     #
#     #     self.btn_connect_to_laser = QPushButton("Connect to Laser")
#     #     self.btn_connect_to_laser.clicked.connect(self._on_connect_clicked)
#     #     self.layout.addWidget(self.btn_connect_to_laser, 1, 2)
#     #
#     #     self.lbl_conn_state = QLabel("Connection State unknown")
#     #     self.layout.addWidget(self.lbl_conn_state, 2, 0)
#     #
#     #     self.layout.addWidget(self.init_UI_wavelength_settings(), 3, 0, 1, 2)
#     #     self.layout.addWidget(self.init_UI_speed_parameters(), 4, 0, 1, 2)
#     #
#     #
#     #
#     #     # widget.setLayout(layout)
#     #     # self.setCentralWidget(widget)
#     #     # self.layout.setLayout(tree)
#     #     self.setWindowTitle("Laser Uncertainty")
#
#     def _on_connect_clicked(self):
#         pass
#
#     def init_UI_wavelength_settings(self, range=[800, 900]):
#         layout = QGridLayout()
#         grid_group_box = QGroupBox("Laser Speed Parameter")
#         grid_group_box.setLayout(layout)
#
#         lbl_wavelength = QLabel("Wavelength")
#         layout.addWidget(lbl_wavelength, 1, 0)
#         self.num_wavelength = QDoubleSpinBox()
#         self.num_wavelength.setRange(-1, range[1])
#         self.num_wavelength.setSingleStep(1)
#         self.num_wavelength.setValue(0)
#         self.num_wavelength.setSuffix(" nm")
#         self.num_wavelength.setDecimals(3)
#         self.num_wavelength.setKeyboardTracking(False)
#         layout.addWidget(self.num_wavelength, 1, 1)
#
#         lbl_sweep_start_wavelength = QLabel("Sweep Start")
#         layout.addWidget(lbl_sweep_start_wavelength, 2, 0)
#         self.num_sweep_start_wavelength = QDoubleSpinBox()
#         self.num_sweep_start_wavelength.setRange(0, 10 ** 9)
#         self.num_sweep_start_wavelength.setSingleStep(1)
#         self.num_sweep_start_wavelength.setValue(0)
#         self.num_sweep_start_wavelength.setSuffix(" nm")
#         self.num_sweep_start_wavelength.setDecimals(3)
#         self.num_sweep_start_wavelength.setKeyboardTracking(False)
#         layout.addWidget(self.num_sweep_start_wavelength, 2, 1)
#
#         lbl_sweep_stop_wavelength = QLabel("Sweep Stop")
#         layout.addWidget(lbl_sweep_stop_wavelength, 3, 0)
#         self.num_sweep_stop_wavelength = QDoubleSpinBox()
#         self.num_sweep_stop_wavelength.setRange(0, 10 ** 9)
#         self.num_sweep_stop_wavelength.setSingleStep(1)
#         self.num_sweep_stop_wavelength.setValue(0)
#         self.num_sweep_stop_wavelength.setSuffix(" nm")
#         self.num_sweep_stop_wavelength.setDecimals(3)
#         self.num_sweep_stop_wavelength.setKeyboardTracking(False)
#         layout.addWidget(self.num_sweep_stop_wavelength, 3, 1)
#
#         self.btn_move_to_wavelength = QPushButton()
#         self.btn_move_to_wavelength.setText("Move to Wavelength")
#         self.btn_move_to_wavelength.clicked.connect(self.move_to_wavelength)
#         layout.addWidget(self.btn_move_to_wavelength, 4, 0, 1, 2)
#
#         return grid_group_box
#
#     def init_UI_speed_parameters(self):
#         layout = QGridLayout()
#         grid_group_box = QGroupBox("Laser Speed Parameter")
#         grid_group_box.setLayout(layout)
#
#         lbl_velocity = QLabel("Velocity")
#         layout.addWidget(lbl_velocity, 1, 0)
#         self.num_velocity = QDoubleSpinBox()
#         self.num_velocity.setRange(-10, 10)
#         self.num_velocity.setSingleStep(1)
#         self.num_velocity.setValue(0)
#         self.num_velocity.setSuffix(" m/s")
#         self.num_velocity.setDecimals(3)
#         self.num_velocity.setKeyboardTracking(False)
#         layout.addWidget(self.num_velocity, 1, 1)
#
#         lbl_acceleration = QLabel("Acceleration")
#         layout.addWidget(lbl_acceleration, 2, 0)
#         self.num_acceleration = QDoubleSpinBox()
#         self.num_acceleration.setRange(-10, 10)
#         self.num_acceleration.setSingleStep(1)
#         self.num_acceleration.setValue(0)
#         self.num_acceleration.setSuffix(" m/s^2")
#         self.num_acceleration.setDecimals(3)
#         self.num_acceleration.setKeyboardTracking(False)
#         layout.addWidget(self.num_acceleration, 2, 1)
#
#         lbl_deceleration = QLabel("Deceleration")
#         layout.addWidget(lbl_deceleration, 3, 0)
#         self.num_deceleration = QDoubleSpinBox()
#         self.num_deceleration.setRange(-10, 10)
#         self.num_deceleration.setSingleStep(1)
#         self.num_deceleration.setValue(0)
#         self.num_deceleration.setSuffix(" m/s^2")
#         self.num_deceleration.setDecimals(2)
#         self.num_deceleration.setKeyboardTracking(False)
#         layout.addWidget(self.num_deceleration, 3, 1)
#         return grid_group_box
#
#     def update_wavelength_param(self, curr, start, stop):
#         self.num_wavelength.setValue(curr)
#         self.num_sweep_start_wavelength.setValue(start)
#         self.num_sweep_stop_wavelength.setValue(stop)
#
#     def update_speed_param(self, vel, acc, dec):
#         self.num_velocity.setValue(vel)
#         self.num_acceleration.setValue(acc)
#         self.num_deceleration.setValue(dec)
#
#     # def move_to_wavelength(self):
#     #    self.laser_controller.start_wavelength_sweep()
