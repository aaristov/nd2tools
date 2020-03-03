import pims_nd2 as nd
import numpy as np
from tqdm.auto import tqdm
from nd2shrink import transform
from tifffile import imread
import logging
import os
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def nd2(path: str, pos_limit=None):
    with nd.ND2_Reader(path,) as frames:
        logger.info(frames.sizes)
        logger.info(frames.metadata)
        json.dump(
            frames.metadata,
            open(path.replace(".nd2", "_meta.json"), "w"),
            default=repr,
        )
        bundle = auto_order(frames.sizes)
        frames.iter_axes = "m"
        frames.bundle_axes = bundle
        for well in tqdm(frames[:pos_limit]):
            yield transform.Well(well, bundle)


def tiff(path: str) -> np.ndarray:
    """ reads .tif to numpy array """
    assert os.path.exists(path)
    assert path.endswith((".tif", ".tiff"))
    tif = imread(path)
    return tif


def auto_order(axes: dict):
    """
    uses nd2.axes dict to output bundle combination
    """
    keys = list(axes.keys())
    default_order = transform.ImageJStack.default_order
    order = list(filter(lambda k: k in keys, default_order))
    return "".join(order)
