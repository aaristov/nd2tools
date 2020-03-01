import matplotlib.pyplot as plt
import numpy as np

from skimage.draw import ellipse
from skimage.transform import rotate

from nd2_combine import segment
import logging

logging.basicConfig(level=logging.DEBUG)

def test_segment():
    image = np.zeros((600, 600))
    cx, cy, b, a = 300, 350, 100, 220
    rr, cc = ellipse(cx, cy, b, a)
    image[rr, cc] = 1.

    mask = segment.findSpheroid(image, plot=0)
    props = segment.get_props(mask)
    np.testing.assert_almost_equal(props['eccentricity'], (1 - b ** 2 / a ** 2) ** 0.5, 2)

