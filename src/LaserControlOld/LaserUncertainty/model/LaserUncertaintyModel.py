from pathlib import Path

import pandas as pd
from PySide6.QtCore import QObject, Signal

from generics.PandasTableModel import PandasTableModel
from mcpy import Uncertainty


class LaserUncertaintyModelSignals(QObject):
    uncertainty_file_changed = Signal(Path)
    calibration_data_changed = Signal(pd.DataFrame)
    uncertainty_changed = Signal(Uncertainty)


class LaserUncertaintyModel(object):
    def __init__(self):
        self.signals = LaserUncertaintyModelSignals()

        # Path to the uncertainty file (measurement data)
        # Expects a csv style file with the expected and actual wavelength
        self._uncertainty_file: Path = None

        # Stores the data from the csv file
        self._calibration_data: pd.DataFrame = None

        # Stores the uncertainty
        self.uncertainty: Uncertainty = None

    @property
    def uncertainty_file(self) -> Path:
        return self._uncertainty_file

    @uncertainty_file.setter
    def uncertainty_file(self, value: Path):
        self._uncertainty_file = value
        self.signals.uncertainty_file_changed.emit(self.uncertainty_file)

    @property
    def calibration_data(self) -> pd.DataFrame:
        return self._calibration_data

    @calibration_data.setter
    def calibration_data(self, value: pd.DataFrame):
        self._calibration_data = value
        self.signals.calibration_data_changed.emit(self.calibration_data)

    @property
    def uncertainty(self) -> Uncertainty:
        return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, value: Uncertainty):
        self._uncertainty = value
        self.signals.uncertainty_changed.emit(self.uncertainty)
