import pims_nd2 as nd
import numpy as np
import scipy
from tqdm.auto import tqdm
from skimage.transform import downscale_local_mean as downscale
from nd2shrink import save
from tifffile import TiffWriter, imread
import logging
import os
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def nd2(path:str, bundle_axes='tyx', pos_limit=None):
    with nd.ND2_Reader(path,) as frames:
        logger.info(frames.sizes)
        logger.info(frames.metadata)
        json.dump(frames.metadata, open(path.replace('.nd2','_meta.json'), 'w'), default=repr)
        frames.iter_axes = 'm'  # 't' is the default already
        frames.bundle_axes = bundle_axes  # when 'z' is available, this will be default
        # frames.default_coords['c'] = channel  # 0 is the default setting
        # frames.default_coords['m'] = well_index
        for well in tqdm(frames[:pos_limit]):
            yield well


def tiff(path:str) -> np.ndarray:
    ''' reads .tif to numpy array '''
    assert os.path.exists(path)
    assert path.endswith(('.tif', '.tiff'))
    tif = imread(path)
    return tif


