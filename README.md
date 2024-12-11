# Laser Control: Python Project for Sacher TEC Laser Control
PySacherECLManager (*Py*thon *Sacher* *E*xternal *C*avity *L*aser) is a Python project developed to control Sacher TEC 
lasers. 
This project offers a convenient interface for users to interact with the laser, adjust parameters, and perform various 
operations for laser control and management.
Features

## Features

- **Laser Parameter Adjustment**: Modify settings such as wavelength and speed for specific requirements.
- **Intuitive GUI**: Easy-to-navigate graphical user interface.
- **Integration Support**: Includes examples for integration with other tools.

## Requirements

- **Python 3.x**: Ensure a compatible version is installed.
- **Sacher TEC Laser Hardware**: Required for functionality.
- **Dependencies**: Listed in the `requirements.txt` file.

## Limitation:
- **Platform**: Currently only tested on Windows.

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/agentsmith29/PySacherECLControl.git
```
### Install dependencies:
The Library requires to have a couple of files that are not directly included in this repository
#### Maxon Motor Driver
1. Maxon Motor drivers as a zip. You can either use the [included zip file](./addtitional_files)
2. Maxon Motor Drivers from the [official website](https://www.maxongroup.de/maxon/view/product/control/Positionierung/380264#)    

#### Sacher Laser Driver
In order to make the library work, you need to include the Sacher Laser Libary, which can be requested by [Sacher]():
1. Set the path to the ```EposCmd64.dll``` and the ```SacherMotorControl.pyd```
```python
conf.epos_dll.set(pathlib.Path(
    f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/EposCmd64.dll'))

conf.motor_control_pyd.set(pathlib.Path(
    f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/'
    f'lib/Python312/SacherMotorControl.pyd'))
```

### Virtual Environment and Dependencies
1. Create a virtual environment (optional, but highly recommended)
```bash
# Create a virtual environment
python -m venv .venv
```
2. Activate the virtual environment
2.1 On Linux and max
```bash
source .venv/bin/activate  # Linux/MacOS
```
2.2 On Windows using cmd
```cmd
.venv\Scripts\activate     # Windows
```
2.3 Alternativily, if you are using Bash on Windows:
```bash
. .venv/Scripts/activate
```

3. Install dependencies
The full list of depdendecies can be found in [```requirements.txt```](./requirements.txt)
``` bash
pip install -r requirements.txt
```

# Usage
## Configuration File
After installing, make sure you create a config. The libary uses the [confpy6](https://github.com/agentsmith29/confPy6) payhton module, to allow working with configuration files, build in the yaml file:
```python
    conf = Laser.Config()
    conf.save()
    #conf.load('./LaserConfig.yaml', as_auto_save=True)
    conf.autosave(True, './LaserConfig.yaml')
```
See (main.py)[./examples/main.py] for an example.
## Base configuration
The base configuration [LaserConfig.py](src/SacherECLControl/LaserConfig.py), gives default vaules for the initialization. These values serve as the default values for initializing the whole application. You should find a similar file after initialization in your startup directory:
```yaml
# - Configuration file stored 2024-11-28 16:28:24.693820 - 
LaserConfig: #!!python/object:controller.LaserConfig
 epos_dll: "@Path:<./EposCmd64.dll>" # epos_dll: None
 motor_control_pyd: "@Path:<./Python312/SacherMotorControl.pyd>" # motor_control_pyd: None
 wl_sweep_start: 845    # wl_sweep_start: None
 wl_sweep_stop: 855     # wl_sweep_stop: None
 velocity: 1.6540566248074888 # velocity: None
 acceleration: 1.9904737652227005 # acceleration: None
 deceleration: 1.9904737652227005 # deceleration: None
 available_ports: ['USB0', 'USB1', 'USB2', 'USB3', 'USB4', 'USB5', 'USB6', 'USB7', 'USB8', 'USB9'] # available_ports: None
 port: "USB0" # port: None
```

## Starting the script
Run the main script. An example can be found in [src](./src)-root:
```bash
python ./src/lasercontrol.py
```
Use the graphical interface to adjust laser parameters, monitor data, and control the laser.
Refer to the user manual or documentation for detailed instructions on specific operations and functionalities.

# Making an exectuable
```bash
source .venv/bin/activate
pip install -r requirements.txt
pyinstaller ./pyinstaller/lasercontrol.spec
```
# Contributing

Contributions to Laser Control are welcome! If you have suggestions for improvements, encounter any issues, or would like to add new features, please feel free to open an issue or submit a pull request on the GitHub repository.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Citing
This project is part of the Software [FlexSensor](https://github.com/agentsmith29/flexsensor) whgich has been published under DOI [10.2139/ssrn.4828876](https://doi.org/10.2139/ssrn.4828876).

Please cite it correctly.
```
Schmidt, Christoph and Hinum-Wagner, Jakob Wilhelm and Klambauer, Reinhard and Bergmann, Alexander, Flexsensor: Automated Measurement Software for Rapid Photonic Circuits Capturing. Available at SSRN: https://ssrn.com/abstract=4828876 or http://dx.doi.org/10.2139/ssrn.4828876 
```
# Acknowledgements
