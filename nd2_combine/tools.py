from glob import glob
import pims_nd2 as nd
import os
import sys
import numpy as np
import logging
from tqdm import tqdm
from nd2tif.transform import Well

logger = logging.getLogger(__name__)


def get_paths(path):
    files = glob(os.path.join(path, "*", "*.nd2"))
    return files


def get_conditions(files):
    return set(sorted([f.split(os.path.sep)[-1].split(".")[0] for f in files]))


def group_input_paths(path, conditions):
    groups = {
        c: {"inputs": sorted(glob(os.path.join(path, "*", f"{c}.nd2")))}
        for c in conditions
    }
    logger.info(f"Groups of {len(groups)} datasets: {groups}")
    return groups


def gen_out_folder_names(path, conditions, subname):
    return {c: os.path.join(path, subname, c) for c in conditions}


def create_out_folder(path, condition, subname="Combined"):
    subpath = os.path.join(path, subname)
    if not os.path.exists(subpath):
        os.mkdir(subpath)
    out_dir = os.path.join(path, subname, condition)
    try:
        os.mkdir(out_dir)
    except FileExistsError:
        logging.warning(f"File exists error: skipping mkdir {out_dir}")
        pass
    return out_dir


def read_nd2(path: str, bundle_axes="yx", pos_limit=None):
    '''
    Reads nd2 file using pims_ND2.ND2_reader
    Yields a dictionary
    {
        "well_index": index,
        "well": well, - single well ('m')
        "order": bundle_axes,
        "calibration_um": px_size_um,
    }
    '''
    logger.debug(f"read_nd2: open {path}")
    with nd.ND2_Reader(path,) as frames:
        logger.debug(frames.sizes)
        # logger.debug(frames.metadata)
        px_size_um = frames.calibration
        frames.iter_axes = "m"
        frames.bundle_axes = bundle_axes
        for index, well in enumerate(frames[:pos_limit]):
            yield {
                "well_index": index,
                "well": well,
                "order": bundle_axes,
                "calibration_um": px_size_um,
            }


def combine_nd2(*paths, out_folder):
    # get handlers to every file
    # iterate by 'm'
    # read first 'm's
    # stack them
    # save tif
    readers = [read_nd2(p) for p in paths]

    logger.info(f'Saving tifs to {os.path.join(out_folder, "Pos_XXX.tif")}')

    for i, images in tqdm(enumerate(zip(*readers))):
        time_series = np.array([im["well"] for im in images], dtype="uint16")
        well = Well(time_series, "tyx", images[0]["calibration_um"])
        logger.debug(time_series.shape)
        path = os.path.join(out_folder, f"Pos_{i:03d}.tif")
        well.save_tif(path)
        logger.debug(f"saving to {path}")


def main():

    subname = "Combined"

    path = sys.argv[-1]
    logger.info(f"processing {path}")

    files = get_paths(path)
    logger.info(f"found {len(files)} datasets: \n{files}")

    conditions = get_conditions(files)
    logger.info(f"Found {len(conditions)} conditions: \n{conditions}")

    inputs = group_input_paths(path, conditions)

    def process_condition(cond):
        logger.info(f"Condition: {cond}")
        out_folder = create_out_folder(path, cond, subname)
        combine_nd2(*inputs[cond]["inputs"], out_folder=out_folder)
        return True

    _ = list(map(process_condition, conditions))
    logger.info("Done processing")

    exit(0)


if __name__ == "__main__":
    main()
