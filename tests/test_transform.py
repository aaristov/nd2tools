import numpy as np
from nd2shrink import transform

def test_auto_shape(
    axes={'x': 2048, 'y': 2044, 'c': 2, 't': 62, 'm': 120},
    order='tzcyxs'
):
    expected_shape = (62, 1, 2, 2044, 2048, 1)
    shape = transform.shape(axes, order)
    np.testing.assert_array_equal(expected_shape, shape)
