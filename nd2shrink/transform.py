import numpy as np
from skimage.transform import downscale_local_mean
from nd2shrink import save
import logging
from nd2reader import ND2Reader

logger = logging.getLogger(__name__)


class ImageJStack:
    default_order = "tzcyxs"
    array = np.ndarray
    order = str
    shape = tuple
    calibration_um = float

    def downscale(self, factor):
        pass

    def to_8bits(self):
        pass

    def save_tif(self, path):
        pass


class Well(ImageJStack):
    def __init__(
        self, array: np.ndarray, order: str, calibration_um: float = None
    ):
        assert array.ndim == len(order)
        self.array = reshape_like_IJ(array, order)
        self.order = ImageJStack.default_order
        self.shape = self.array.shape
        self.calibration_um = calibration_um

    def downscale(self, factor):
        array = downscale_local_mean(self.array, (1, 1, 1, factor, factor, 1))
        return Well(array, self.order, self.calibration_um * factor)

    def to_8bits(self):
        arr = self.array.astype("f")
        lim_shape = list(self.shape)
        lim_shape[3:] = [1, 1, 1]
        lim_shape[0] = 1
        lim_shape = tuple(lim_shape)
        _min = arr.min(axis=(0, 3, 4)).reshape(lim_shape)
        _max = arr.max(axis=(0, 3, 4)).reshape(lim_shape)
        logger.debug(f"min/max: {_min}/{_max}")
        new_array = (arr - _min) * 255 / (_max - _min)
        return Well(new_array.astype("uint8"), self.order, self.calibration_um)

    def save_tif(self, path):
        save.tiff(path, self.array, self.calibration_um)


def reshape_like_IJ(array: np.ndarray, order: str):
    assert [d in (ij := ImageJStack.default_order) for d in order], f'Order {order} in incompatible with IJ {ij}'
    assert array.ndim == len(order), f'Order {order} in incompatible with array ndim {array.shape}'
    dim_diff = len(ij) - len(order)
    shape = tuple([1] * dim_diff + list(array.shape))
    rarray = array.reshape(shape)
    assert rarray.ndim == len(ij)
    from_order = np.arange(dim_diff, rarray.ndim)
    to_order = [ij.index(d) for d in order]
    print(from_order, to_order)
    sarray = np.moveaxis(rarray, from_order, to_order)
    return sarray




def shape(sizes: dict, order: str = "tzcyxs"):
    """
    Generates a good shape for imagej tif stack.

    Parameters:
    -----------
    sizes: dict
        nd2.sizes dict
    order: str
        axis order in imagej. Default 'tzcyxs'
    """

    keys = list(sizes.keys())
    shape = [1] * len(order)

    for k in keys:
        try:
            shape[order.index(k)] = sizes[k]
        except ValueError:
            pass

    return tuple(shape)


def scale_down(well: np.ndarray, factor=4):
    """
    Downscales xy coordinates by factor
    """
    logger.debug(f"scale down well {well.shape} {well.ndim}d")
    vector = tuple([1] * (well.ndim - 2) + [factor] * 2)
    logger.debug(f"vector {vector}")
    try:
        ds_well = downscale_local_mean(well, vector).astype("uint16")
    except Exception as e:
        logger.error(f"unable to downscalse with vector {vector}")
        raise e
    logger.debug(f"scale xy {well.shape} -> {ds_well.shape}")
    return ds_well


def recursive_downscale(file: ND2Reader, axes: list, sizes: dict, mod):
    '''
    recursively reads axes of nd2
    '''

    arr = []
    ax = axes.pop()
    print(f'ax: {ax}, axes: {axes}')
    size = sizes[ax]
    if len(axes) > 0:
        for a in range(size):
            print(f'{ax}: {a+1}/{size}')
            file.default_coords[ax] = a
            res = recursive_downscale(file, axes, sizes, mod)
            arr.append(res)
        return np.array(arr, dtype=res.dtype)
    else:
        file.iter_axes = ax
        for yx in file:
            print('.', end='')
            res = mod(yx)
            arr.append(res)
        print(len(arr), yx.shape, ' -> ', res.shape)
        axes.append(ax)
        return np.array(arr, dtype=yx.dtype)
