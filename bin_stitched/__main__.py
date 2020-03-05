from pims_nd2 import ND2_Reader
import numpy as np
import sys
from nd2shrink import transform


def main(path, factor=16):
    file = ND2_Reader(path)
    print(file.sizes)
    tczyx = []
    try:
        time = file.sizes['t']
    except KeyError:
        time = 1
    try:
        channels = file.sizes['c']
    except KeyError:
        channels = 1
    for t in range(time):
        czyx = []
        print('c', end=' ')
        for c in range(channels):
            print(f'\rc{c}', end='')
            if channels > 1:
                file.default_coords['c']=c
            data = file[t]
            assert data.ndim == 3
            scaled = transform.scale_down(data, factor)
            czyx.append(scaled)
        tczyx.append(czyx)
        print(f'\rt{t+1}/{time}', '.'*(t+1))
    print('done reading')
    tczyx_np = np.array(tczyx, dtype=scaled.dtype)
    print(tczyx_np.shape)
    w = transform.Well(tczyx_np, 'tczyx', file.calibration * factor)
    save_path = path.replace('.nd2', '_downscale_16x.tif')
    w.save_tif(save_path)
    print(f'saved to {save_path}')
    return True


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        OK = main(path)
        if OK:
            exit(0)
        else:
            exit(2)
    except IndexError:
        print('Please provide .nd2 path. Exiting')
        exit(1)
