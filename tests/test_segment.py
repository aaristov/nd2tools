import matplotlib.pyplot as plt
import numpy as np

from skimage.draw import ellipse
from skimage.transform import rotate

from segment import seg
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def test_segment():
    image = np.zeros((600, 600))
    cx, cy, b, a = 300, 350, 50, 100
    rr, cc = ellipse(cx, cy, b, a)
    image[rr, cc] = 1.0

    mask = seg.find_spheroid(image, plot=0)
    props = seg.get_props(mask)
    logger.debug(f"len(props) {len(props)}")
    np.testing.assert_almost_equal(
        props[0]["eccentricity"], (1 - b ** 2 / a ** 2) ** 0.5, 0.02
    )
