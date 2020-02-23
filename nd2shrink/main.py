import numpy
from libtiff import TIFFimage

if __name__ == "__main__":
        
    im = TIFFimage(numpy.zeros((10,10), dtype='uint16'))
    im.write_file('zeros.tif', compression='lzw')

    exit(0)