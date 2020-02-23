from nd2shrink import read, save
import sys
import os
import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    args = sys.argv
    path = args[-1]

    if os.path.exists(path) and path.endswith('.nd2'):
        reader = read.nd2(path, bundle_axes='tcyx', pos_limit=2)

        new_path = path.replace('.nd2', '_downscale_4x.tif')

        save.tiff(new_path, reader, rescale=4, to_8bits=False)

    else:
        print('Provide valid .nd2 path')