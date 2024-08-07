import ctypes
import os
import pathlib
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# from SacherECLControl.controller.LaserCon import LaserCon
dll_dir = pathlib.Path(
    f"{os.path.dirname(os.path.realpath(__file__))}/libs/SacherLib/PythonMotorControlClass/EposCMD64.dll")
dll_dir = str(dll_dir.resolve())
dll_dest = f"{os.getcwd()}/EposCMD64.dll"
# Copy the file "EposCMD64.dll" to the current dir
if not  pathlib.Path(dll_dest).exists():
    shutil.copyfile(dll_dir, f"{os.getcwd()}/EposCMD64.dll")

from WidgetCollection.Tools.PyProjectExtractor import extract_pyproject_info

# Directly in the repo
pytoml = pathlib.Path(__file__).parent.parent.parent
if not pytoml.exists():
    # if installed via pip
    pytoml = pathlib.Path(__file__).parent

__version__ = extract_pyproject_info(pytoml, "version")
__author__ = extract_pyproject_info(pytoml, "author")
__description__ = extract_pyproject_info(pytoml, "description")
__license__ = extract_pyproject_info(pytoml, "license")
__url__ = extract_pyproject_info(pytoml, "url")

# For correctly display the icon in the taskbar
myappid = f'agentsmith29.SacherECLControl.{__version__}'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from .controller.LaserDeviceControl import MPLaserDeviceControl as Controller
from .model.LaserControlModel import LaserControlModel as Model
from .view.LaserControlView import LaserControlView as View
from .LaserConfig import LaserConfig as Config

