import numpy
from tifffile import TiffWriter, imsave
from nd2shrink import transform
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def tiff(fname:str, array:numpy.ndarray):
    imsave(fname, array, imagej=True)
    return True
