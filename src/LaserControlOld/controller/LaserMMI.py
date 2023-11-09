import logging

#if velox_config.VeloxConfigOD.use_simulator:
 #  import flexsensorpy.simulator.sim_velox as velox_api

# import velox.view.main_window as main_window

from flexsensorpy.model.laserdriver import LaserDriver




class LaserSacherMMI(LaserDriver):

    def __init__(self, start_file: str) -> None:
        self.logger = logging.Logger("Sacher Laser")

        if start_file is None:
            raise ValueError("Sacher Laser Start file must not be None")
        self.set_start_file(start_file)

    def set_start_file(self, start_file):
        self.start_file = start_file
        self.logger.info(f"Setting start file to {self.start_file}")

    @staticmethod
    def generate_start_script():
        pass

    def start_wavelength_sweep(self):
        '''
        Start a wavelength sweep
        '''
        self.logger.info("Start wavelength sweep")
        try:
            with open(self.start_file, "a") as f:
                f.write("\n")
        except Exception as e:
            self.logger.error(f"Error writing to Sacher Laser start file {self.start_file}: {e}")
            raise e

        return True

    @staticmethod
    def train_laser(iteration: int = 100):

        # To train the laser we are doing the following
        # 1. Set the laser to 850 nm
        # 2. Start a wavelength sweep
        LaserSacherMMI.start_wavelength_sweep()
        # Measure the signal
        #