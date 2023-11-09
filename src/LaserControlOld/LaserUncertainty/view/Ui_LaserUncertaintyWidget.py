# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LaserUncertaintyWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_LaserUncertaintyWidget(object):
    def setupUi(self, LaserUncertaintyWidget):
        if not LaserUncertaintyWidget.objectName():
            LaserUncertaintyWidget.setObjectName(u"LaserUncertaintyWidget")
        LaserUncertaintyWidget.resize(500, 624)
        LaserUncertaintyWidget.setMinimumSize(QSize(500, 600))
        self.gridLayout_2 = QGridLayout(LaserUncertaintyWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridFrame = QFrame(LaserUncertaintyWidget)
        self.gridFrame.setObjectName(u"gridFrame")
        self.gridFrame.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.vlo_measurement = QFrame(self.gridFrame)
        self.vlo_measurement.setObjectName(u"vlo_measurement")
        self.vlo_measurement.setMaximumSize(QSize(16777215, 150))
        self.verticalLayout = QVBoxLayout(self.vlo_measurement)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.table_measurement_data = QTableView(self.vlo_measurement)
        self.table_measurement_data.setObjectName(u"table_measurement_data")
        self.table_measurement_data.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout.addWidget(self.table_measurement_data)


        self.gridLayout.addWidget(self.vlo_measurement, 2, 0, 1, 1)

        self.plot_area = QVBoxLayout()
        self.plot_area.setObjectName(u"plot_area")

        self.gridLayout.addLayout(self.plot_area, 1, 0, 1, 1)

        self.hlo_csv_path_2 = QFrame(self.gridFrame)
        self.hlo_csv_path_2.setObjectName(u"hlo_csv_path_2")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hlo_csv_path_2.sizePolicy().hasHeightForWidth())
        self.hlo_csv_path_2.setSizePolicy(sizePolicy)
        self.hlo_csv_path_2.setMaximumSize(QSize(16777215, 40))
        self.gridLayout_3 = QGridLayout(self.hlo_csv_path_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.hlo_csv_path_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 24))
        self.label.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.text_csv_data_path = QLineEdit(self.hlo_csv_path_2)
        self.text_csv_data_path.setObjectName(u"text_csv_data_path")
        self.text_csv_data_path.setMinimumSize(QSize(0, 24))
        self.text_csv_data_path.setMaximumSize(QSize(16777215, 24))

        self.gridLayout_3.addWidget(self.text_csv_data_path, 0, 1, 1, 1)

        self.btn_load_cal_data = QPushButton(self.hlo_csv_path_2)
        self.btn_load_cal_data.setObjectName(u"btn_load_cal_data")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_load_cal_data.sizePolicy().hasHeightForWidth())
        self.btn_load_cal_data.setSizePolicy(sizePolicy1)
        self.btn_load_cal_data.setMinimumSize(QSize(24, 24))
        self.btn_load_cal_data.setMaximumSize(QSize(24, 24))

        self.gridLayout_3.addWidget(self.btn_load_cal_data, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.hlo_csv_path_2, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.gridFrame, 0, 0, 1, 1)


        self.retranslateUi(LaserUncertaintyWidget)

        QMetaObject.connectSlotsByName(LaserUncertaintyWidget)
    # setupUi

    def retranslateUi(self, LaserUncertaintyWidget):
        LaserUncertaintyWidget.setWindowTitle(QCoreApplication.translate("LaserUncertaintyWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("LaserUncertaintyWidget", u"CSV Path", None))
        self.btn_load_cal_data.setText(QCoreApplication.translate("LaserUncertaintyWidget", u"...", None))
    # retranslateUi

