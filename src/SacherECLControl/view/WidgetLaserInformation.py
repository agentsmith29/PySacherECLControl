from PySide6.QtWidgets import QGridLayout, QGroupBox, QLabel, QWidget

from WidgetCollection.widgets.LEDIndicatorWidget import LEDIndicatorWidget


class WidgetLaserInformation(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.init_UI()



    def init_UI(self):
        rid_group_box = QGroupBox("Capturing Information")
        layout = QGridLayout()



        # Connection state
        self.lbl_conn_state = QLabel("Not connected")
        self.led_conn_state = LEDIndicatorWidget(color="red")
        layout.addWidget(self.led_conn_state, 0, 0)
        layout.addWidget(self.lbl_conn_state, 0, 1)

        # Flag i s moving
        self.lbl_laser_is_moving = QLabel("Laser not moving")
        self.led_laser_is_moving = LEDIndicatorWidget(color="red")
        layout.addWidget(self.led_laser_is_moving, 1, 0)
        layout.addWidget(self.lbl_laser_is_moving, 1, 1)

        # Device state
        #self.lbl_device_state = QLabel("No faults (not connected)")
        #self.led_device_state = LEDIndicatorWidget(color="gray")
        #layout.addWidget(self.led_device_state, 2, 0)
        #layout.addWidget(self.lbl_device_state, 2, 1)

        # Connection state
        self.lbl_capt_device = QLabel("No Capturing device connected")
        self.led_capt_device = LEDIndicatorWidget(color="red")
        layout.addWidget(self.led_capt_device, 2, 0)
        layout.addWidget(self.lbl_capt_device, 2, 1)


        #grid_group_box.setLayout(layout)
        #self.layout.addWidget(layout)
        self.setLayout(layout)

    def set_connection_state(self, state: bool, text: str = None):
        if state:
            self.led_conn_state.set_color("green")
            if text is not None:
                self.lbl_conn_state.setText(text)
            else:
                self.lbl_conn_state.setText("Connected")
        else:
            self.led_conn_state.set_color("red")
            if text is not None:
                self.lbl_conn_state.setText(text)
            else:
                self.lbl_conn_state.setText("Not connected")

    def set_movement_state(self, state: bool, text: str = None):
        if state:
            self.led_laser_is_moving.set_color("green")
            if text is not None:
                self.lbl_laser_is_moving.setText(text)
            else:
                self.lbl_laser_is_moving.setText("Laser moving")
        else:
            self.led_laser_is_moving.set_color("red")
            if text is not None:
                self.lbl_laser_is_moving.setText(text)
            else:
                self.lbl_laser_is_moving.setText("Laser not moving")


    def set_capt_dev_state(self, state: bool, text: str = None):
        if state:
            self.led_capt_device.set_color("green")
            if text is not None:
                self.lbl_capt_device.setText(text)
            else:
                self.lbl_capt_device.setText("Laser moving")
        else:
            self.led_capt_device.set_color("red")
            if text is not None:
                self.lbl_capt_device.setText(text)
            else:
                self.lbl_capt_device.setText("Laser not moving")