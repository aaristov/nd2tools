import nd2reader as nd
import numpy as np
import sys
from nd2shrink import transform


def main(path, factor=16):
    file = nd.ND2Reader(path)
    print(file.sizes)
    tczyx = []
    for t in range(file.sizes['t']):
        print(f't: {t}')
        file.default_coords['t'] = t
        czyx = []
        for c in range(file.sizes['c']):
            print(f'c {c}')
            file.default_coords['c'] = c
            file.iter_axes = 'z'
            zyx = []
            print('z', end='')
            for yx in file:
                print('.', end='')
                dyx = transform.scale_down(yx, factor=factor)
                zyx.append(dyx)
            czyx.append(zyx)
            print(len(czyx), len(zyx), dyx.shape)
        tczyx.append(czyx)
    tczyx_np = np.array(tczyx, dtype=yx.dtype)
    print(tczyx_np.shape)
    w = transform.Well(tczyx_np, 'tczyx', file.metadata['pixel_microns'] * factor)
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
