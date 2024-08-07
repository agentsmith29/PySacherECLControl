import os
import pathlib
import sys
from ctypes import CDLL, cdll

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

dir = pathlib.Path(f"{os.path.dirname(os.path.realpath(__file__))}")
dir = str(dir.resolve().as_posix())
print(dir)