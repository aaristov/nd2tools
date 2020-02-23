from nd2shrink import save
import numpy
from nd2shrink import read

import os, sys

def test_save_zeros():
    arr = numpy.random.randint(0, 2**12, (20,256,256), dtype='uint16')

    OK = save.tiff('zeros.tif', arr, 'none')

    assert os.path.exists('zeros.tif')

# def read_zeros():
    tif = read.tiff('zeros.tif')
    # array = numpy.array([t for t in tif.iter_images()])
    numpy.testing.assert_array_equal(arr, tif)
    # tif.close()





