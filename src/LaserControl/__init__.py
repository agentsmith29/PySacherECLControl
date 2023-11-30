import logging
import os
import sys

from rich.logging import RichHandler


# check if a handler is already set
#if not logging.root.handlers:
#    FORMAT = "%(name)s %(message)s"
#    logging.basicConfig(
#        level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
#            RichHandler(rich_tracebacks=True)
#        ]
#    )

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


from .controller.LaserControlController import LaserControlController as Controller
from .model.LaserControlModel import LaserControlModel as Model
from .view.LaserControlView import LaserControlView as View
from .LaserConfig import LaserConfig as Config