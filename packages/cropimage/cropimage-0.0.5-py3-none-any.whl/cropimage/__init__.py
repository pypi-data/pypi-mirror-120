import os
import sys
from .cropper import Cropper

__title__ = "cropimage"
__description__ = "Automatically crops main body from pictures"
__author__ = "Haofan Wang"
__version__ = "0.0.5"


# Inject vendored directory into system path.
v_path = os.path.abspath(
    os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), "vendor"])
)
sys.path.insert(0, v_path)

# Inject patched directory into system path.
v_path = os.path.abspath(
    os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), "patched"])
)
sys.path.insert(0, v_path)