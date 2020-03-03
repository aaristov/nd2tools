import numpy as np
import pims_nd2 as nd
import json
import logging


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


def detect_wells(zyx: np.ndarray):
    pass
