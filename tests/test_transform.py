# TODO: test class methods instead

import numpy as np
from numpy.testing import assert_array_equal
from nd2shrink import transform, read
from scipy.ndimage import binary_erosion
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_auto_order(
    axes={"x": 2048, "y": 2044, "c": 2, "t": 62, "m": 120}, order="tzcyxs"
):
    expected_order = "tcyx"
    order = read.auto_order(axes)
    assert expected_order == order


def test_auto_shape(
    axes={"x": 2048, "y": 2044, "c": 2, "t": 62, "m": 120}, order="tzcyxs"
):
    expected_shape = (62, 1, 2, 2044, 2048, 1)
    shape = transform.shape(axes, order)
    np.testing.assert_array_equal(expected_shape, shape)


def test_scale_down():
    arr = np.ones((8, 8))
    arr[::2] = -1
    s_arr = transform.scale_down(arr, factor=2)
    np.testing.assert_array_equal((4, 4), s_arr.shape)
    np.testing.assert_array_equal(np.zeros((4, 4)), s_arr)


def test_scale_big():
    big_shape = (8858, 7103)
    factor = 16
    padding = tuple(int(s % factor > 0) for s in big_shape)
    expected_d16 = tuple(s // factor + p for s, p in zip(big_shape, padding))
    test_array = np.zeros(big_shape)
    d16_array = transform.scale_down(test_array, factor=int(factor))
    np.testing.assert_array_equal(d16_array.shape, expected_d16)


def test_reshape_like_IJ():
    arr = np.ones((2, 4, 5))
    order = "zyx"
    expected_shape = (1, 2, 1, 4, 5, 1)  # tzcyxs
    ij_arr = transform.reshape_like_IJ(arr, order)
    np.testing.assert_array_equal(expected_shape, ij_arr.shape)


def test_reshape_like_IJ_slicing():
    x, y, z, c, t = (400, 600, 8, 3, 10)
    dtype = 'uint8'
    border = 10
    factor = 10
    dx, dy = x//factor, y//factor
    dborder = border//factor

    xy = np.ones((y, x), dtype=dtype)
    xy_border = binary_erosion(xy, iterations=border)
    logger.debug(xy_border)
    assert_array_equal(xy_border[:border], np.zeros((border, x)))
    assert_array_equal(xy_border[-border:], np.zeros((border, x)))
    assert_array_equal(xy_border[:, :border], np.zeros((y, border)))
    assert_array_equal(xy_border[:, -border:], np.zeros((y, border)))

    zyx_border = np.array([xy_border]*z, dtype=dtype)
    assert_array_equal(zyx_border.shape, (z, y, x))

    dzxy = transform.scale_down(zyx_border, factor=factor)
    assert_array_equal(dzxy.shape, (z, dy, dx))
    assert_array_equal(dzxy[:, :dborder], np.zeros((z, dborder, dx)))
    assert_array_equal(dzxy[:, -dborder:], np.zeros((z, dborder, dx)))
    assert_array_equal(dzxy[:, :, :dborder], np.zeros((z, dy, dborder)))
    assert_array_equal(dzxy[:, :, -dborder:], np.zeros((z, dy, dborder)))

    czyx_border = np.array([zyx_border]*c, dtype=dtype)
    assert_array_equal(czyx_border.shape, (c, z, y, x))

    tczyx_border = np.array([czyx_border]*t, dtype=dtype)
    assert_array_equal(tczyx_border.shape, (t, c, z, y, x))

    ij_arr = transform.Well(tczyx_border, 'tczyx', 1)
    assert_array_equal(ij_arr.array.shape, (t, z, c, y, x, 1))
    assert_array_equal(ij_arr.array[0, 0, 0, 0], np.zeros((x, 1)))
    assert_array_equal(ij_arr.array[0, 0, 0, :, 0], np.zeros((y, 1)))
    assert_array_equal(ij_arr.array[0, 0, 0, border:-border, border:-border], np.ones((y-2*border, x-2*border, 1)))

