import numpy
from tifffile import TiffWriter, imwrite
from nd2shrink import transform
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def tiff(fname:str, array:numpy.ndarray, calibration_um:float=None):
    if (c := calibration_um):
        imwrite(fname, array, imagej=True, resolution=(1/c, 1/c), metadata={'unit': 'um'})
    else:
        imwrite(fname, array, imagej=True)
    return True
