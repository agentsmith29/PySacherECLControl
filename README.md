# Laser Control: Python Project for Sacher TEC Laser Control
PySacherECLManager (*Py*thon *Sacher* *E*xternal *C*avity *L*aser) is a Python project developed to control Sacher TEC 
lasers. 
This project offers a convenient interface for users to interact with the laser, adjust parameters, and perform various 
operations for laser control and management.
Features

* Laser Parameter Adjustment: Laser Control allows users to adjust parameters such as wavelength and speed settings.
* User-friendly Interface: The project offers an intuitive graphical user interface (GUI) for easy navigation and control.
* Works with the Analog Discovery 2 driver: 
Requirements

* Python 3.x
* Sacher TEC laser hardware (compatible models)
* Dependencies specified in requirements.txt

#  Installation

    Clone the repository:
```bash
git clone https://github.com/agentsmith29/fs.lasercontrol.git
```
## Install dependencies:
## Place the Sacher Laser Library in your working directory
```bash

# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
. .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

After installing, you need to set the pathes to the Sacher Libaray using 
the `config.py` file. 

```python
    conf = Laser.Config()
    conf.save()
    #conf.load('./LaserConfig.yaml', as_auto_save=True)
    conf.autosave(True, './LaserConfig.yaml')
    
    # Set the path to the EposCmd64.dll and the SacherMotorControl.pyd
    conf.epos_dll.set(pathlib.Path(
    f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/EposCmd64.dll'))
    
    conf.motor_control_pyd.set(pathlib.Path(
    f'{Laser.__rootdir__}/libs/SacherLib/PythonMotorControlClass/'
    f'lib/Python312/SacherMotorControl.pyd'))
```
See (main.py)[./examples/main.py] for an example.

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

# Citing
This project is part of the Software [FlexSensor](https://github.com/agentsmith29/flexsensor) whgich has been published under DOI [10.2139/ssrn.4828876](https://doi.org/10.2139/ssrn.4828876).

Please cite it correctly.
```
Schmidt, Christoph and Hinum-Wagner, Jakob Wilhelm and Klambauer, Reinhard and Bergmann, Alexander, Flexsensor: Automated Measurement Software for Rapid Photonic Circuits Capturing. Available at SSRN: https://ssrn.com/abstract=4828876 or http://dx.doi.org/10.2139/ssrn.4828876 
```
# Acknowledgements
