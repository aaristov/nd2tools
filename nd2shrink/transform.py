import numpy as np
from skimage.transform import downscale_local_mean
import logging

logger = logging.getLogger(__name__)

def shape(sizes:dict, order:str = 'tzcyxs'):
    '''
    Generates a good shape for imagej tif stack.

    Parameters:
    -----------
    sizes: dict
        nd2.sizes dict
    order: str
        axis order in imagej. Default 'tzcyxs'
    '''

    keys = list(sizes.keys())
    shape = [1] * len(order)

    for k in keys:
        try:
            shape[order.index(k)] = sizes[k]
        except ValueError:
            pass

    return tuple(shape)


def scale_down(well:np.ndarray, factor=4):
    '''
    Downscales xy coordinates by factor
    '''
    vector = tuple([1] * (well.ndim - 2) + [factor] * 2)
    ds_well = downscale_local_mean(well, vector).astype('uint16')
    logger.debug(f'scale xy {well.shape} -> {ds_well.shape}')
    return ds_well


def rescale_16_8bits(array:np.ndarray):
    '''
    Reduce 16 to 8 bits with normalization
    '''
    assert array.dtype == np.uint16, f'assertion error {array.dtype}'
    arr = array.astype('f')
    _min, _max = arr.min(), arr.max()
    logger.debug(f'min/max: {_min}/{_max}')
    new_array = (arr - _min) * 255 / (_max - _min)
    return new_array.astype('uint8')

