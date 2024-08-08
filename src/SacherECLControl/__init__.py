import ctypes
import os
import pathlib
import shutil
import sys

from WidgetCollection.Tools.PyProjectExtractor import extract_pyproject_info

from . import Helpers

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))



# ======================================================================================================================
# The pyconfig.toml file is needed, to get the metadata. Depending on the installation method (pip or git) the file
# is found in different places.
# ======================================================================================================================
pytoml = Helpers.get_pyprojecttoml()
def try_and_set(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error reading '{args[1]}' from {pathlib.Path(args[0])}: {e}")
        return "unknown"

__rootdir__ = os.path.dirname(os.path.realpath(__file__))
__version__ = try_and_set(extract_pyproject_info, pytoml.parent, "version")
__author__ = try_and_set(extract_pyproject_info, pytoml.parent, "author")
__description__ = try_and_set(extract_pyproject_info, pytoml.parent, "description")
__license__ = try_and_set(extract_pyproject_info, pytoml.parent, "license")
__url__ = try_and_set(extract_pyproject_info, pytoml.parent, "url")

# For correctly display the icon in the taskbar
myappid = f'agentsmith29.SacherECLControl.{__version__}'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from .controller.LaserDeviceControl import MPLaserDeviceControl as Controller
from .model.LaserControlModel import LaserControlModel as Model
from .view.LaserControlView import LaserControlView as View
from .LaserConfig import LaserConfig as Config
