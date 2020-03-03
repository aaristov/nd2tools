from nd2shrink import read, save
import sys
import os
import logging

logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)


def main(path, rescale=4, to_8bits=True):
    if not os.path.exists(path) or not path.endswith(".nd2"):
        logger.error("Provide valid .nd2 path")
        return False

    reader = read.nd2(path, pos_limit=2)

    new_path = path.replace(".nd2", f"_downscale_{rescale}x.tif")

    for i, well in enumerate(reader):
        ds_well = well.downscale(rescale)
        if to_8bits:
            ds_well = ds_well.to_8bits()
        name = new_path.replace(".tif", f"_Pos_{i:03d}.tif")
        save.tiff(name, ds_well.array)
    return True


if __name__ == "__main__":
    args = sys.argv
    path = args[-1]

    main(path)
