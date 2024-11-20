# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LaserControlWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLCDNumber, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSlider, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)
from . import resources_rc

class Ui_LaserControlWindow(object):
    def setupUi(self, LaserControlWindow):
        if not LaserControlWindow.objectName():
            LaserControlWindow.setObjectName(u"LaserControlWindow")
        LaserControlWindow.resize(697, 717)
        self.centralwidget = QWidget(LaserControlWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"QWidget{\n"
"    background-color: rgb(40, 44, 52);\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Q"
                        "TableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::se"
                        "ction:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizo"
                        "ntal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-r"
                        "adius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     he"
                        "ight: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* ///////////////////////////////////////////////////////////"
                        "//////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(52, 59, 72);\n"
"	border-radius: 2px;\n"
"	border: 1px solid rgb(0, 0, 0);\n"
"}\n"
"QComboBox:hover{\n"
"	border: 1px solid rgb(42, 175, 211);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 2px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius"
                        ": 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"/*QComboBox QAbstractItemView::item {\n"
"  min-height: 150px;\n"
"}*/\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(0, 0, 0);\n"
"    border: 1px solid rgb(42, 175, 211);\n"
"    height: 10px;\n"
"    width: 8px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider"
                        "::handle:horizontal:hover {\n"
"    background-color: rgb(42, 141, 211);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(42, 141, 211);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
""
                        "QCommandLinkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"QPushButton {\n"
"	border: 1px solid rgb(42, 175, 211);\n"
"	border-radius: 2px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 1px solid rgb(42, 141, 211);\n"
"    border-radius: 2px;	\n"
"	background-color: rgb(42, 141, 211);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 1px solid rgb(42, 141, 211);\n"
"    border-radius: 2px;	\n"
"	background-color: rgb(35, 40, 49);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"/* QMenu ------------------------------------------------------------------"
                        "\n"
"\n"
"examples: https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmenu\n"
"\n"
"--------------------------------------------------------------------------- */\n"
"QMenu {\n"
"    background-color: rgb(40, 44, 52);\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"\n"
"QMenu::item {\n"
"    padding: 2px 25px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    border-color: darkblue;\n"
"    background: rgba(100, 100, 100, 150);\n"
"}\n"
"\n"
"QMenu::icon:checked { /* appearance of a 'checked' icon */\n"
"    background: gray;\n"
"    border: 1px inset gray;\n"
"    position: absolute;\n"
"    top: 1px;\n"
"    right: 1px;\n"
"    bottom: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    height: 2px;\n"
"    background: lightblue;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"}\n"
"\n"
"QTabWidge"
                        "t::pane {\n"
"  border: 1px solid lightgray;\n"
"  top:-1px; \n"
"  background:  rgb(40, 44, 52); \n"
"} \n"
"\n"
"QTabBar::tab {\n"
"  background: rgb(40, 44, 52);; \n"
"  border: 1px solid lightgray; \n"
"  padding: 2px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background:  rgb(189, 147, 249);\n"
"  margin-bottom: -1px; \n"
"}\n"
"")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.table_laser_control = QTabWidget(self.centralwidget)
        self.table_laser_control.setObjectName(u"table_laser_control")
        self.tab_control = QWidget()
        self.tab_control.setObjectName(u"tab_control")
        self.gridLayout_9 = QGridLayout(self.tab_control)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.grd_tab_settings = QGridLayout()
        self.grd_tab_settings.setObjectName(u"grd_tab_settings")
        self.group_motor_profile = QGroupBox(self.tab_control)
        self.group_motor_profile.setObjectName(u"group_motor_profile")
        self.group_motor_profile.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_motor_profile.sizePolicy().hasHeightForWidth())
        self.group_motor_profile.setSizePolicy(sizePolicy)
        self.group_motor_profile.setMinimumSize(QSize(0, 0))
        self.group_motor_profile.setMaximumSize(QSize(16777215, 150))
        self.gridLayout_7 = QGridLayout(self.group_motor_profile)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(-1, -1, 0, 0)
        self.lbl_vel = QLabel(self.group_motor_profile)
        self.lbl_vel.setObjectName(u"lbl_vel")

        self.gridLayout_11.addWidget(self.lbl_vel, 0, 0, 1, 1)

        self.lbl_acc = QLabel(self.group_motor_profile)
        self.lbl_acc.setObjectName(u"lbl_acc")

        self.gridLayout_11.addWidget(self.lbl_acc, 1, 0, 1, 1)

        self.sb_velocity = QDoubleSpinBox(self.group_motor_profile)
        self.sb_velocity.setObjectName(u"sb_velocity")
        self.sb_velocity.setEnabled(True)
        self.sb_velocity.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)

        self.gridLayout_11.addWidget(self.sb_velocity, 0, 1, 1, 1)

        self.sb_acc = QDoubleSpinBox(self.group_motor_profile)
        self.sb_acc.setObjectName(u"sb_acc")
        self.sb_acc.setEnabled(True)
        self.sb_acc.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)

        self.gridLayout_11.addWidget(self.sb_acc, 1, 1, 1, 1)

        self.lbl_dec = QLabel(self.group_motor_profile)
        self.lbl_dec.setObjectName(u"lbl_dec")

        self.gridLayout_11.addWidget(self.lbl_dec, 2, 0, 1, 1)

        self.sb_dec = QDoubleSpinBox(self.group_motor_profile)
        self.sb_dec.setObjectName(u"sb_dec")
        self.sb_dec.setEnabled(True)
        self.sb_dec.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)

        self.gridLayout_11.addWidget(self.sb_dec, 2, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_11)


        self.gridLayout_7.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.grd_tab_settings.addWidget(self.group_motor_profile, 3, 0, 1, 2)

        self.group_wavelength_settings = QGroupBox(self.tab_control)
        self.group_wavelength_settings.setObjectName(u"group_wavelength_settings")
        self.group_wavelength_settings.setMinimumSize(QSize(0, 210))
        self.group_wavelength_settings.setMaximumSize(QSize(16777215, 300))
        self.gridLayout_5 = QGridLayout(self.group_wavelength_settings)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.lbl_wavelength = QLabel(self.group_wavelength_settings)
        self.lbl_wavelength.setObjectName(u"lbl_wavelength")

        self.gridLayout_12.addWidget(self.lbl_wavelength, 3, 0, 1, 1)

        self.btn_move_to_wavelength = QPushButton(self.group_wavelength_settings)
        self.btn_move_to_wavelength.setObjectName(u"btn_move_to_wavelength")

        self.gridLayout_12.addWidget(self.btn_move_to_wavelength, 5, 0, 1, 2)

        self.sb_set_wavelength = QDoubleSpinBox(self.group_wavelength_settings)
        self.sb_set_wavelength.setObjectName(u"sb_set_wavelength")
        self.sb_set_wavelength.setMinimumSize(QSize(150, 0))

        self.gridLayout_12.addWidget(self.sb_set_wavelength, 3, 1, 1, 1)

        self.lcd_wavelength = QLCDNumber(self.group_wavelength_settings)
        self.lcd_wavelength.setObjectName(u"lcd_wavelength")
        self.lcd_wavelength.setEnabled(True)
        self.lcd_wavelength.setMinimumSize(QSize(0, 62))
        self.lcd_wavelength.setMaximumSize(QSize(16777215, 62))
        self.lcd_wavelength.setFrameShape(QFrame.Shape.Box)
        self.lcd_wavelength.setFrameShadow(QFrame.Shadow.Sunken)
        self.lcd_wavelength.setLineWidth(1)
        self.lcd_wavelength.setMidLineWidth(0)
        self.lcd_wavelength.setSmallDecimalPoint(True)
        self.lcd_wavelength.setDigitCount(10)
        self.lcd_wavelength.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcd_wavelength.setProperty("value", 830.000000000000000)
        self.lcd_wavelength.setProperty("intValue", 830)

        self.gridLayout_12.addWidget(self.lcd_wavelength, 9, 0, 1, 2)

        self.gridWidget = QWidget(self.group_wavelength_settings)
        self.gridWidget.setObjectName(u"gridWidget")
        self.gridWidget.setMaximumSize(QSize(16777215, 50))
        self.gridLayout_2 = QGridLayout(self.gridWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lbl_max_wavelength = QLabel(self.gridWidget)
        self.lbl_max_wavelength.setObjectName(u"lbl_max_wavelength")
        self.lbl_max_wavelength.setMaximumSize(QSize(16777215, 18))
        self.lbl_max_wavelength.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lbl_max_wavelength.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.lbl_max_wavelength, 1, 1, 1, 1)

        self.lbl_min_wavelength = QLabel(self.gridWidget)
        self.lbl_min_wavelength.setObjectName(u"lbl_min_wavelength")
        self.lbl_min_wavelength.setMaximumSize(QSize(16777215, 18))
        self.lbl_min_wavelength.setMargin(0)

        self.gridLayout_2.addWidget(self.lbl_min_wavelength, 1, 0, 1, 1)

        self.slider_wavelength = QSlider(self.gridWidget)
        self.slider_wavelength.setObjectName(u"slider_wavelength")
        self.slider_wavelength.setMinimumSize(QSize(0, 10))
        self.slider_wavelength.setOrientation(Qt.Orientation.Horizontal)
        self.slider_wavelength.setInvertedControls(False)
        self.slider_wavelength.setTickPosition(QSlider.TickPosition.NoTicks)

        self.gridLayout_2.addWidget(self.slider_wavelength, 0, 0, 1, 2)


        self.gridLayout_12.addWidget(self.gridWidget, 6, 0, 1, 2)


        self.gridLayout_5.addLayout(self.gridLayout_12, 0, 0, 1, 1)


        self.grd_tab_settings.addWidget(self.group_wavelength_settings, 1, 0, 1, 2)

        self.group_sweep_settings = QGroupBox(self.tab_control)
        self.group_sweep_settings.setObjectName(u"group_sweep_settings")
        self.group_sweep_settings.setMinimumSize(QSize(250, 0))
        self.group_sweep_settings.setMaximumSize(QSize(16777215, 90))
        self.gridLayout_8 = QGridLayout(self.group_sweep_settings)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.sb_sweep_stop = QDoubleSpinBox(self.group_sweep_settings, decimals=2)
        self.sb_sweep_stop.setObjectName(u"sb_sweep_stop")

        self.gridLayout_10.addWidget(self.sb_sweep_stop, 0, 3, 1, 1)

        self.lbl_sweep_start = QLabel(self.group_sweep_settings)
        self.lbl_sweep_start.setObjectName(u"lbl_sweep_start")
        self.lbl_sweep_start.setMinimumSize(QSize(100, 0))

        self.gridLayout_10.addWidget(self.lbl_sweep_start, 0, 0, 1, 1)

        self.lbl_sweep_stop = QLabel(self.group_sweep_settings)
        self.lbl_sweep_stop.setObjectName(u"lbl_sweep_stop")
        self.lbl_sweep_stop.setMinimumSize(QSize(100, 0))

        self.gridLayout_10.addWidget(self.lbl_sweep_stop, 0, 2, 1, 1)

        self.btn_start_sweep = QPushButton(self.group_sweep_settings)
        self.btn_start_sweep.setObjectName(u"btn_start_sweep")

        self.gridLayout_10.addWidget(self.btn_start_sweep, 1, 0, 1, 4)

        self.sb_sweep_start = QDoubleSpinBox(self.group_sweep_settings, decimals=2)
        self.sb_sweep_start.setObjectName(u"sb_sweep_start")

        self.gridLayout_10.addWidget(self.sb_sweep_start, 0, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_10, 1, 0, 1, 1)


        self.grd_tab_settings.addWidget(self.group_sweep_settings, 2, 0, 1, 2)

        self.grp_system_info = QGroupBox(self.tab_control)
        self.grp_system_info.setObjectName(u"grp_system_info")
        self.grp_system_info.setMinimumSize(QSize(0, 110))
        self.grp_system_info.setMaximumSize(QSize(16777215, 110))
        self.gridLayout_6 = QGridLayout(self.grp_system_info)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.grd_system_info = QGridLayout()
        self.grd_system_info.setObjectName(u"grd_system_info")

        self.gridLayout_6.addLayout(self.grd_system_info, 0, 0, 1, 1)


        self.grd_tab_settings.addWidget(self.grp_system_info, 0, 1, 1, 1)

        self.grp_Connection = QGroupBox(self.tab_control)
        self.grp_Connection.setObjectName(u"grp_Connection")
        self.grp_Connection.setMinimumSize(QSize(250, 100))
        self.grp_Connection.setMaximumSize(QSize(300, 110))
        self.gridLayout_4 = QGridLayout(self.grp_Connection)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.vgrd_connection_settings = QVBoxLayout()
        self.vgrd_connection_settings.setObjectName(u"vgrd_connection_settings")
        self.lbl_port_selection = QLabel(self.grp_Connection)
        self.lbl_port_selection.setObjectName(u"lbl_port_selection")
        self.lbl_port_selection.setMaximumSize(QSize(16777215, 12))

        self.vgrd_connection_settings.addWidget(self.lbl_port_selection)

        self.cb_port_selection = QComboBox(self.grp_Connection)
        self.cb_port_selection.setObjectName(u"cb_port_selection")

        self.vgrd_connection_settings.addWidget(self.cb_port_selection)

        self.btn_connect = QPushButton(self.grp_Connection)
        self.btn_connect.setObjectName(u"btn_connect")

        self.vgrd_connection_settings.addWidget(self.btn_connect)


        self.gridLayout_4.addLayout(self.vgrd_connection_settings, 0, 0, 1, 1)


        self.grd_tab_settings.addWidget(self.grp_Connection, 0, 0, 1, 1)


        self.gridLayout_9.addLayout(self.grd_tab_settings, 0, 0, 1, 1)

        self.table_laser_control.addTab(self.tab_control, "")
        self.tab_uncertainty = QWidget()
        self.tab_uncertainty.setObjectName(u"tab_uncertainty")
        self.grd_uncertainty = QGridLayout(self.tab_uncertainty)
        self.grd_uncertainty.setObjectName(u"grd_uncertainty")
        self.table_laser_control.addTab(self.tab_uncertainty, "")
        self.tab_uncertainty_dist = QWidget()
        self.tab_uncertainty_dist.setObjectName(u"tab_uncertainty_dist")
        self.grd_uncertainty_dist = QGridLayout(self.tab_uncertainty_dist)
        self.grd_uncertainty_dist.setObjectName(u"grd_uncertainty_dist")
        self.table_laser_control.addTab(self.tab_uncertainty_dist, "")

        self.gridLayout_3.addWidget(self.table_laser_control, 2, 0, 1, 1)

        self.horizontalFrame = QFrame(self.centralwidget)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        self.horizontalFrame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.horizontalLayout = QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.menuBar = QFrame(self.horizontalFrame)
        self.menuBar.setObjectName(u"menuBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menuBar.sizePolicy().hasHeightForWidth())
        self.menuBar.setSizePolicy(sizePolicy1)
        self.menuBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.menuBar)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.menu_file = QToolButton(self.menuBar)
        self.menu_file.setObjectName(u"menu_file")

        self.horizontalLayout_2.addWidget(self.menu_file)

        self.menu_edit = QToolButton(self.menuBar)
        self.menu_edit.setObjectName(u"menu_edit")

        self.horizontalLayout_2.addWidget(self.menu_edit)

        self.menu_run = QToolButton(self.menuBar)
        self.menu_run.setObjectName(u"menu_run")

        self.horizontalLayout_2.addWidget(self.menu_run)


        self.horizontalLayout.addWidget(self.menuBar)

        self.horizontalFrame1 = QFrame(self.horizontalFrame)
        self.horizontalFrame1.setObjectName(u"horizontalFrame1")
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalFrame1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.horizontalLayout.addWidget(self.horizontalFrame1)


        self.gridLayout_3.addWidget(self.horizontalFrame, 0, 0, 1, 1)

        LaserControlWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LaserControlWindow)

        self.table_laser_control.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LaserControlWindow)
    # setupUi

    def retranslateUi(self, LaserControlWindow):
        LaserControlWindow.setWindowTitle(QCoreApplication.translate("LaserControlWindow", u"MainWindow", None))
        self.group_motor_profile.setTitle(QCoreApplication.translate("LaserControlWindow", u"Motor Profile", None))
        self.lbl_vel.setText(QCoreApplication.translate("LaserControlWindow", u"Velocity", None))
        self.lbl_acc.setText(QCoreApplication.translate("LaserControlWindow", u"Acceleration", None))
        self.sb_velocity.setSuffix(QCoreApplication.translate("LaserControlWindow", u" nm/s", None))
        self.sb_acc.setSuffix(QCoreApplication.translate("LaserControlWindow", u" nm/s^2", None))
        self.lbl_dec.setText(QCoreApplication.translate("LaserControlWindow", u"Deceleration", None))
        self.sb_dec.setSuffix(QCoreApplication.translate("LaserControlWindow", u" nm/s^2", None))
        self.group_wavelength_settings.setTitle(QCoreApplication.translate("LaserControlWindow", u"Wavelength", None))
        self.lbl_wavelength.setText(QCoreApplication.translate("LaserControlWindow", u"Wavelength [nm]", None))
        self.btn_move_to_wavelength.setText(QCoreApplication.translate("LaserControlWindow", u"Move", None))
        self.sb_set_wavelength.setSuffix(QCoreApplication.translate("LaserControlWindow", u"nm", None))
        self.lbl_max_wavelength.setText(QCoreApplication.translate("LaserControlWindow", u"870 nm", None))
        self.lbl_min_wavelength.setText(QCoreApplication.translate("LaserControlWindow", u"830 nm", None))
        self.group_sweep_settings.setTitle(QCoreApplication.translate("LaserControlWindow", u"Sweep Settings", None))
        self.sb_sweep_stop.setSuffix(QCoreApplication.translate("LaserControlWindow", u" nm", None))
        self.lbl_sweep_start.setText(QCoreApplication.translate("LaserControlWindow", u"Sweep Start [nm]", None))
        self.lbl_sweep_stop.setText(QCoreApplication.translate("LaserControlWindow", u"Sweep Stop [nm]", None))
        self.btn_start_sweep.setText(QCoreApplication.translate("LaserControlWindow", u"Start Sweep", None))
        self.sb_sweep_start.setSuffix(QCoreApplication.translate("LaserControlWindow", u" nm", u"nm/s"))
        self.grp_system_info.setTitle(QCoreApplication.translate("LaserControlWindow", u"System Information", None))
        self.grp_Connection.setTitle(QCoreApplication.translate("LaserControlWindow", u"Connection Settings", None))
        self.lbl_port_selection.setText(QCoreApplication.translate("LaserControlWindow", u"USB Port Connection", None))
        self.btn_connect.setText(QCoreApplication.translate("LaserControlWindow", u"Connect", None))
        self.table_laser_control.setTabText(self.table_laser_control.indexOf(self.tab_control), QCoreApplication.translate("LaserControlWindow", u"Laser Control", None))
        self.table_laser_control.setTabText(self.table_laser_control.indexOf(self.tab_uncertainty), QCoreApplication.translate("LaserControlWindow", u"Uncertainty", None))
        self.table_laser_control.setTabText(self.table_laser_control.indexOf(self.tab_uncertainty_dist), QCoreApplication.translate("LaserControlWindow", u"Uncertainty Distribution", None))
        self.menu_file.setText(QCoreApplication.translate("LaserControlWindow", u"File", None))
        self.menu_edit.setText(QCoreApplication.translate("LaserControlWindow", u"Edit", None))
        self.menu_run.setText(QCoreApplication.translate("LaserControlWindow", u"Run", None))
    # retranslateUi

