import numpy as np
import pims_nd2 as nd
import json
import logging
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def read_stitched_nd2(path: str, bundle="zyx", channel=0, time_limit=None):
    """
    Reads nd2 with bundle, channel
    Yields one timepoint at a time.
    """

    with nd.ND2_Reader(path,) as frames:
        logger.info(frames.sizes)
        # logger.info(frames.calibration)
        # logger.info(frames.calibrationZ)

        # json.dump(frames.metadata, open(path.replace('.nd2','_meta.json'), 'w'), default=repr)
        frames.iter_axes = "t"
        frames.default_coords["c"] = channel
        frames.bundle_axes = bundle
        for zyx in frames[:time_limit]:
            yield zyx


def detect_wells(bf: np.ndarray, thr=0.1, sigma=2, erode=5, plot=False):
    grad = get_2d_gradient(bf)
    sm_grad = gaussian_filter(grad, sigma)
    mask = sm_grad > sm_grad.max() * thr
    filled_mask = binary_erosion(binary_fill_holes(mask), structure=np.ones((erode,erode)))

    if plot:
        [show(b) for b in [grad, sm_grad, mask, filled_mask]]

    return filled_mask


def get_2d_gradient(xy):
    gx, gy = np.gradient(xy)
    return np.sqrt(gx ** 2 + gy ** 2)


def show(grad, **kwargs):
    plt.figure(figsize=(15, 10))
    plt.imshow(grad, cmap='gray', **kwargs)
