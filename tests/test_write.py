from nd2shrink import save
import numpy
from nd2shrink import read

import os, sys

def test_save_zeros():
    arr = numpy.random.randint(0, 2**12, (20,256,256), dtype='uint16')

    _ = save.tiff('zeros.tif', arr)

    assert os.path.exists('zeros.tif')

    tif = read.tiff('zeros.tif')
    numpy.testing.assert_array_equal(arr, tif)





