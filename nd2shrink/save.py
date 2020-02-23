from libtiff import TIFFimage
import numpy
from tifffile import TiffWriter, imsave
from nd2shrink import transform
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def tiff(fname:str, reader, rescale=4, to_8bits=True):
    for i, well in enumerate(reader):
        ds_well = transform.scale_down(well, rescale)
        if to_8bits:
            ds_well = transform.rescale_16_8bits(ds_well)
        name = fname.replace('.tif',f'_Pos_{i:03d}.tif')
        # ds_well.shape = 
        imsave(name, ds_well, imagej=True) #TZCYXS order
    return True


def __tiff(fname:str, array:numpy.ndarray, compression='none'):
    '''
    Saves the tif file
    Parameters:
    -----------

    fname, str:
        file path

    array, numpy.ndarray:
        input array

    compression, str
        'none' or 'lzw'
    '''
    im = TIFFimage(array)
    im.write_file('zeros.tif', compression='none')
    return True

def append_tiff(path, reader, rescale=4):

    # print(f'{well.shape} -> {ds_well.shape}')
    # out = np.array(ds_wells, dtype='uint16')
    # print(out.dtype)
    # print(out.shape)
    with TiffWriter(path, bigtiff=True, byteorder=None, append=False, imagej=False) as tif:
        for well in reader:
            ds_well = transform.scale_down(well, rescale)
            tif.save(ds_well)
    logger.info(f'Saved to {path}')
    return True