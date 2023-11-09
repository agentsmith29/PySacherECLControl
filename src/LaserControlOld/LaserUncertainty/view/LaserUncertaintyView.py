import logging
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Laser.LaserUncertainty.model.LaserUncertaintyModel import LaserUncertaintyModel
from Laser.LaserUncertainty.view.Ui_LaserUncertaintyWidget import Ui_LaserUncertaintyWidget
from generics.PandasTableModel import PandasTableModel
from mcpy.userinterface.UncertaintyWidget import UncertaintyWidget


class LaserUncertaintyView(QWidget):

    def __init__(self, model: LaserUncertaintyModel, parent = None, logger=None):
        super().__init__()
        self.model: LaserUncertaintyModel = model
        if logger is None and parent is None:
            self.logger = logging.getLogger(__name__)
        elif logger is None and parent is not None and hasattr(parent, "logger"):
            self.logger = parent.logger

        self._ui = Ui_LaserUncertaintyWidget()
        self._ui.setupUi(self)

        # Add the Plot Area
        self.uncertainty_plot_figure = plt.Figure()
        self.plot_canvas = FigureCanvas(self.uncertainty_plot_figure)
        self._ui.plot_area.addWidget(self.plot_canvas)



        # Connect Signal and Slots
        self.model.signals.calibration_data_changed.connect(self._on_calibration_data_changed)
        self.model.signals.uncertainty_file_changed.connect(self._on_uncertainty_file_changed)


        self._ui.btn_load_cal_data.clicked.connect(self._on_btn_load_cal_data_clicked)

        self._uncertainty_file = None

    def _on_btn_load_cal_data_clicked(self):
        # Create a file selection dialog
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog(self, options=options)
        file_dialog.setWindowTitle("Select Data File")
        file_dialog.setNameFilter("CSV files (*.txt);;All Files (*)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.model.uncertainty_file = selected_files[0]
                self.logger.info(f"Loading calibration data from file: {self.model.uncertainty_file}")


        # self.laser_uncertainty.plot_data(self.laser_controller.uncertainty.calibration_data)

    def _plot_uncertainty_data(self, data):
        x, y = data['wavelength_set'], data['wavelength_diff']

        # Clear the previous plot (if any)
        self.uncertainty_plot_figure.clear()

        # Plot the data using Matplotlib
        ax = self.uncertainty_plot_figure.add_subplot(111)
        ax.plot(x, y, 'r', label='Wavelength Deviation')
        ax.set_xlabel('Motorposition')
        ax.set_ylabel('Value')
        ax.legend()

        # Refresh the canvas
        self.plot_canvas.draw()

    def _on_uncertainty_file_changed(self, measurement_files):
        self._ui.text_csv_data_path.setText(measurement_files)

    def _on_calibration_data_changed(self, data):
        self._ui.table_measurement_data.setModel(PandasTableModel(self.model.calibration_data))
        self._plot_uncertainty_data(data)


