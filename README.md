# Laser Control: Python Project for Sacher TEC Laser Control
LaserControl is a Python project developed to control Sacher TEC lasers. This project offers a convenient interface for users to interact with the laser, adjust parameters, and perform various operations for laser control and management.
Features

* Laser Parameter Adjustment: Laser Control allows users to adjust parameters such as wavelength and speed settings.
* User-friendly Interface: The project offers an intuitive graphical user interface (GUI) for easy navigation and control.
* Works with the Analog Discovery 2 driver: 
Requirements

* Python 3.x
* Sacher TEC laser hardware (compatible models)
* Dependencies specified in requirements.txt

#  Installation

## Device Drivers
### Maxon Motor Drivers
Install the required Maxon Motor drivers:
The Maxon Motor drivers are required to communicate with the Sacher TEC laser hardware. The Sacher laser 
has a Maxon EPOS2 digital positioning controller. The drivers can be downloaded from the Maxon website. 
The installation instructions are available in the user manual or documentation provided by Maxon. 
[EPOS USB Driver Installation](https://www.maxongroup.com/maxon/view/product/control/Positionierung/390438)

A up-to-date (08/2024) release can also be found in this repository [here (2.12.28.0)](./addtitional_files/EPOS-USB-Driver-Installation-En_2.12.28.0.zip)

### Analog Discovery 2/3 Drivers
If the Laser Controller is used with the Analog Discovery 2/3, the WaveForms SDK must be installed.
See the readme of the corresponding repository for installation instructions.
https://github.com/agentsmith29/fs.captdevicecontrol

It should be sufficient to install the [WaveForms SDK](https://reference.digilentinc.com/reference/software/waveforms/waveforms-sdk/start)
from the Digilent website.

## Installation and Setup
Clone the repository:
```bash
git clone https://github.com/agentsmith29/fs.lasercontrol.git
```
The library for controlling the software can be found in
[./src/LaserControl/libs/Python*/SacherMotorControl.pyd](./src/LaserControl/libs)
Place the correct Sacher-Laser-Library (*SacherMotorControl.pyd*) in your working directory.
This library may be changed and thus can be updated and so far is only available for Windows.

Create a new environment and install the dependencies:
```bash
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
. .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

# Usage

Run the main script:

```bash
python examples/main.py
```
Use the graphical interface to adjust laser parameters, monitor data, and control the laser.
Refer to the user manual or documentation for detailed instructions on specific operations and functionalities.

# Contributing

Contributions to Laser Control are welcome! If you have suggestions for improvements, encounter any issues, or would like to add new features, please feel free to open an issue or submit a pull request on the GitHub repository.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgements