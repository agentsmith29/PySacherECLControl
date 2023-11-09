import numpy as np
import pandas as pd
from scipy.stats import stats

from Laser.LaserUncertainty.model.LaserUncertaintyModel import LaserUncertaintyModel
from Laser.LaserUncertainty.view.LaserUncertaintyView import LaserUncertaintyView
from mcpy import DirectObservations
from mcpy.TypeBUncertainty.Normal import Normal
from mcpy.TypeBUncertainty.Rectangular import Rectangular


class LaserUncertaintyController(object):

    def __init__(self, model: LaserUncertaintyModel, view: LaserUncertaintyView):
        self.model: LaserUncertaintyModel = model
        self.view: LaserUncertaintyView = view

        # Connect signals and slots
        self.model.signals.uncertainty_file_changed.connect(self._on_uncertainty_file_changed)

    def read_measurement_file(self, measurement_files):
        # Read the measurement file
        self.calibration_data = pd.read_csv(self.model.uncertainty_file, delimiter='\t', decimal=',')
        # Rename the columns
        self.calibration_data = self.calibration_data.rename(columns={'Motorposition': 'motor_position',
                                                                      'WL theo': 'wavelength_set',
                                                                      'WL act': 'wavelength_measured',
                                                                      'Motorschlag': 'Motorschlag'})

        self.calibration_data['wavelength_set'] = pd.to_numeric(
            self.calibration_data['wavelength_set'], errors='coerce')
        self.calibration_data['wavelength_measured'] = pd.to_numeric(
            self.calibration_data['wavelength_measured'], errors='coerce')
        self.calibration_data = self.calibration_data.replace([np.inf, -np.inf], np.nan).dropna(axis=0).reset_index()

        # substract columen WL theo from WL act
        self.calibration_data['wavelength_diff'] = self.calibration_data['wavelength_set'] - self.calibration_data['wavelength_measured']

        # Filter outliers using stats.zscore
        self.calibration_data['zscore'] = stats.zscore(self.calibration_data['wavelength_diff'])
        self.model.calibration_data = self.calibration_data.loc[self.calibration_data['zscore'].abs() < 3]

        self.model.uncertainty = DirectObservations(observations=np.array(self.model.calibration_data['wavelength_diff']), k=3)

    def _on_uncertainty_file_changed(self, measurement_files):
        self.read_measurement_file(measurement_files)
        #self._ui.table_measurement_data.setModel(self.laser_uncertainty.qt_table)
        #self._ui.text_csv_data_path.setText(measurement_files)

