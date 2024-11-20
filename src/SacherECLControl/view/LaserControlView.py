import logging
import os

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtWidgets import QMainWindow, QProgressDialog, QToolButton, QMenu
from WidgetCollection.Dialogs import AboutDialog
from rich.logging import RichHandler

from SacherECLControl.controller.LaserDeviceControl import MPLaserDeviceControl
from SacherECLControl.model.LaserControlModel import LaserControlModel
from SacherECLControl.view.Ui_LaserControlWindow import Ui_LaserControlWindow
from SacherECLControl.view.WidgetLaserInformation import WidgetLaserInformation


from SacherECLControl import __version__, __author__, __license__, __description__, __url__
class LaserControlView(QMainWindow):

    def __init__(self, model: LaserControlModel, controller: MPLaserDeviceControl):
        super().__init__()

        self.logger = controller.logger

        self._ui = Ui_LaserControlWindow()
        self._ui.setupUi(self)

        self.setWindowTitle(f'Sacher External Cavity Laser Control - {__version__}')
        self.setWindowIcon(QIcon(':/icons/icons/sacherelccontrol_icon.png'))

        self.about_dialog = AboutDialog(
            "ADScope Control",
            __description__,
            __version__,
            f"2024 {__author__}",
            __url__,
            f"This project is open source and contributions are highly welcome.<br>"
            f"<br>The project is licensed under <br>{__license__}.",
            QPixmap(':/icons/icons/sacherelccontrol_icon.png')
        )

        self._init_menu_bar()

        self._enable_ui(enabled=False)

        self.laser_moving_progress_dialog = QProgressDialog(self)
        self.laser_moving_progress_dialog.cancel()
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_timer)

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

    # def _on_uncertainty_changed(self, uncertainty):
    #    self.uncertainty_dist_plot.uncertainty = uncertainty

    def _init_menu_bar(self):
        # Add menu bar
        self.file_menu = QMenu('&Files', self)

        self.act_connect = QAction('Connect', self)
        self.file_menu.addAction(self.act_connect)

        self.file_menu.addSeparator()

        self.file_menu.addSeparator()

        self.act_about = QAction('About', self)
        self.act_about.triggered.connect(self.about_dialog.exec)
        self.file_menu.addAction(self.act_about)

        self.act_exit = QAction('Exit', self)
        self.act_exit.setShortcut('Ctrl+Q')
        self.file_menu.addAction(self.act_exit)

        self._ui.menu_file.setMenu(self.file_menu)
        self._ui.menu_file.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

    def connect_capturing_device(self, device):
        pass

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

        #self._ui.btn_save_velocity_params.clicked.connect(self._on_btn_save_velocity_params_clicked)
        self._ui.sb_velocity.editingFinished.connect(self._on_sb_velocity_editing_finished)
        self._ui.sb_acc.editingFinished.connect(self._on_sb_acc_editing_finished)
        self._ui.sb_dec.editingFinished.connect(self._on_sb_dec_editing_finished)

    def _connect_signals(self):

        # Triggerd if the laser connection status changes
        self.model.signals.connected_changed.connect(self._on_laser_connected_changed)
        self.model.signals.laser_is_moving_changed.connect(self._on_laser_is_moving_changed)

        # Capturing device signals
        self.model.signals.capturing_device_connected_changed.connect(self._on_capture_device_connected_changed)

        # self.uncertainty_model.signals.uncertainty_changed.connect(self._on_uncertainty_changed)

        # Triggerd if the laser port changes
        self.model.signals.current_wavelength_changed.connect(self._on_wavelength_changed)
        self.model.signals.min_laser_wavelength_changed.connect(self._on_min_wavelength_changed)
        self.model.signals.max_laser_wavelength_changed.connect(self._on_max_wavelength_changed)

        self.model.signals.velocity_changed.connect(self._on_velocity_changed)
        self.model.signals.acceleration_changed.connect(self._on_acceleration_changed)
        self.model.signals.deceleration_changed.connect(self._on_deceleration_changed)

        # Sweep Settings
        self.model.signals.sweep_start_wavelength_changed.connect(self._on_sweep_start_changed)
        self.model.signals.sweep_stop_wavelength_changed.connect(self._on_sweep_stop_changed)

        # ==================================================================================================================
        # Slots that are triggerd if the laser connection changes
        # ==================================================================================================================

    def _enable_ui(self, enabled=True):
        self._ui.group_motor_profile.setEnabled(enabled)
        self._ui.group_wavelength_settings.setEnabled(enabled)
        self._ui.group_sweep_settings.setEnabled(enabled)

    def _on_laser_connected_changed(self, connected):
        if connected:
            self._ui.btn_connect.setText("Disconnect")
            self.laser_information.set_connection_state(True, f"Connected ({self.model.port})")
        else:
            self._ui.btn_connect.setText("Connect")
            self.laser_information.set_connection_state(False)
        self._enable_ui(connected)

    def _on_laser_is_moving_changed(self, is_moving, to_wl):
        self._ui.btn_move_to_wavelength.setEnabled(not is_moving)
        self._ui.btn_start_sweep.setEnabled(not is_moving)
        self.laser_information.set_movement_state(is_moving, "Moving" if is_moving else "Stopped")
        if is_moving:
            self.logger.info(f"Moving from {self.model.current_wavelength} nm to  {to_wl} nm")
            self._display_estimated_progress(
                self.model.current_wavelength,
                self.model.laser_moving_to_wavelength)
        else:
            self._exit_display_estimated_progress()

    # ==================================================================================================================
    # Slots that are triggerd if the laser settings change7
    # ==================================================================================================================
    #def _on_connected_changed(self, connected):
    #    self.laser_information.set_connection_state(connected)
    #

    # ==================================================================================================================
    # Slots that are triggered if the capturing device changes
    # ==================================================================================================================
    def _on_capture_device_connected_changed(self, connected):
        if connected:
            self.laser_information.set_capt_dev_state(connected, self.model.capturing_device.model.device_information.device_name)
            self.model.capturing_device.model.device_information.signals.device_name_changed.connect(
                self._on_capture_device_name_changed)

    def _on_capture_device_name_changed(self):
        self.laser_information.set_capt_dev_state(self.model.capturing_device_connected,
                                                  f"Connected: {self.model.capturing_device.model.device_information.device_name}")

    def _on_wavelength_changed(self, wavelength):
        self.logger.debug(f"Wavelength changed to: {wavelength}. "
                    f"Range ({self.model.min_laser_wavelength}-{self.model.max_laser_wavelength})nm")

        # self._ui.lbl_min_wavelength.setText(str(self.model.min_laser_wavelength))
        # self._ui.lbl_max_wavelength.setText(str(self.model.max_laser_wavelength))

        # self._ui.slider_wavelength.setMinimum(self.model.min_laser_wavelength)
        # self._ui.slider_wavelength.setMaximum(self.model.max_laser_wavelength)

        # self._ui.sb_set_wavelength.setMinimum(self.model.min_laser_wavelength)
        # self._ui.sb_set_wavelength.setMaximum(self.model.max_laser_wavelength)

        # Set the minimum and maximum values for the sweep start and stop
        #self._ui.sb_set_wavelength.setValue(wavelength)
        self._ui.lcd_wavelength.display(wavelength)
        self._ui.slider_wavelength.setValue(wavelength)

    def _on_min_wavelength_changed(self, min_wavelength):
        self._ui.lbl_min_wavelength.setText(str(self.model.min_laser_wavelength))
        self._ui.slider_wavelength.setMinimum(self.model.min_laser_wavelength)
        self._ui.sb_set_wavelength.setMinimum(self.model.min_laser_wavelength)

    def _on_max_wavelength_changed(self, min_wavelength):
        self._ui.lbl_max_wavelength.setText(str(self.model.max_laser_wavelength))
        self._ui.slider_wavelength.setMaximum(self.model.max_laser_wavelength)
        self._ui.sb_set_wavelength.setMaximum(self.model.max_laser_wavelength)

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
        self.logger.debug(f"View: Sweep start changed. "
                          f"Min {self.model.min_laser_wavelength}, Max {self.model.max_laser_wavelength}")
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
            self.controller.disconnect_device()
        elif not self.model.connected:
            self.logger.debug(f"Attempting to connect to laser on port: {self.model.port}")
            self.controller.connect_device(usb_port=self.model.port)


    def _on_btn_move_to_wavelength_clicked(self):
        self.logger.debug(f"Attempting to set wavelength to: {self._ui.sb_set_wavelength.value()}")
        self.controller.move_to_wavelength(
            self.model.port,
            self._ui.sb_set_wavelength.value())

    def _on_sb_sweep_start_changed(self, value):
        try:
            self.logger.debug(f"Sweep start changed. New Range {value}-{self.model.sweep_stop_wavelength}")
            self.model.sweep_start_wavelength = float(value)
        except Exception as e:
            self.logger.error(e)
            self.model.sweep_start_wavelength = float(value)

    def _on_sb_sweep_stop_changed(self, value):
        try:
            self.logger.debug(f"Sweep stop changed. New Range {self.model.sweep_start_wavelength}-{value}")
            self.model.sweep_stop_wavelength = float(value)
        except Exception as e:
            self.logger.error(e)
            self.model.sweep_stop_wavelength = float(value)
        # self.controller.set_sweep_wavelength_range(self._ui.sb_sweep_start.value(), self._ui.sb_sweep_stop.value())

    def _on_btn_start_sweep_clicked(self):
        self.logger.warning("Sweep manually started")
        self.controller.start_wavelength_sweep.emit(self.model.sweep_start_wavelength, self.model.sweep_stop_wavelength)

    def _on_sb_velocity_editing_finished(self):
        self.controller.set_velocity(self._ui.sb_velocity.value())

    def _on_sb_acc_editing_finished(self):
        self.controller.set_acceleration(self._ui.sb_acc.value())

    def _on_sb_dec_editing_finished(self):
        self.controller.set_deceleration(self._ui.sb_dec.value())

    def _on_btn_save_velocity_params_clicked(self):
        self.controller.set_velocity(self._ui.sb_velocity.value())
        self.controller.set_acceleration(self._ui.sb_acc.value())
        self.controller.set_deceleration(self._ui.sb_dec.value())

    def _display_estimated_progress(self, start_wavelength: float, stop_wavelength: float):

        # Dialog that displays the estimated time until the sweep is finished
        # calulate the time, the laser accelerates using
        self.laser_moving_progress_dialog.show()
        et_acc_dec = self.model.velocity / self.model.acceleration
        wl_after_acc = start_wavelength + 0.5 * self.model.acceleration * et_acc_dec ** 2
        wl_bevore_dec = stop_wavelength - 0.5 * self.model.deceleration * et_acc_dec ** 2
        if wl_bevore_dec > wl_after_acc:
            self.eta = 2 * et_acc_dec + (wl_bevore_dec - wl_after_acc) / self.model.velocity
        else:
            self.eta = 2 * et_acc_dec + (wl_after_acc - wl_bevore_dec) / self.model.velocity


        self.laser_moving_progress_dialog.setLabelText(
            f"Laser is moving {start_wavelength}-{stop_wavelength}."
            f"\nEstimated time until sweep is finished: {self.eta}")
        steps_per_second = self.eta / 100
        self.timer.start(steps_per_second * 1000)

    def _exit_display_estimated_progress(self):
        self.timer.stop()
        self.laser_moving_progress_dialog.close()

    def handle_timer(self):
        value = self.laser_moving_progress_dialog.value() + 1
        self.laser_moving_progress_dialog.setValue(value)

    def closeEvent(self, event):
        # do stuff
        self.controller.safe_exit()
