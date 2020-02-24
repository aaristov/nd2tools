# TODO: test class methods instead

import numpy as np
from nd2shrink import transform, read
import logging

logging.basicConfig(level=logging.DEBUG)

def test_auto_order(
    axes={'x': 2048, 'y': 2044, 'c': 2, 't': 62, 'm': 120},
    order='tzcyxs'):
    expected_order = 'tcyx'
    order = read.auto_order(axes)
    assert expected_order == order


def test_auto_shape(
    axes={'x': 2048, 'y': 2044, 'c': 2, 't': 62, 'm': 120},
    order='tzcyxs'
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

def test_reshape_like_IJ():
    arr = np.ones((2,4,5))
    order = 'zyx'
    expected_shape = (1,2,1,4,5,1) # tzcyxs
    ij_arr = transform.reshape_like_IJ(arr, order)
    np.testing.assert_array_equal(expected_shape, ij_arr.shape)

