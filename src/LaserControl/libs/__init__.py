import os
import pathlib
import sys
from ctypes import CDLL, cdll

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

dir = pathlib.Path(f"{os.path.dirname(os.path.realpath(__file__))}")
dir = str(dir.resolve().as_posix())
print(dir)


with os.add_dll_directory(dir):
    #os.environ['PATH'] = dir + os.pathsep + os.environ['PATH']
    #cdll.LoadLibrary("EposCmd64.dll")
    from .LaserLib import *