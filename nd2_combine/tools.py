from glob import glob
import pims_nd2 as nd
import os, sys
import numpy as np
from tifffile import imsave
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

def get_paths(path):
    files = glob(os.path.join(path, '*', '*.nd2'))
    return files

def get_conditions(files):
    return set([f.split('\\')[-1].split('.')[0] for f in files])

def combine_input_files(path, conditions):
    return {c: {'inputs': glob(path + rf'\*\{c}.nd2')} for c in conditions}

def gen_out_folder_names(path, conditions, subname):
    return {c: os.path.join(path, subname, c) for c in conditions}

def create_out_folder(path, condition, subname='Combined'):
    subpath = os.path.join(path, subname)
    if not os.path.exists(subpath):
        os.mkdir(subpath)
    out_dir = os.path.join(path, subname, condition)
    try:
        os.mkdir(out_dir)
    except FileExistsError:
        logging.warning(f'File exists error: skipping mkdir {out_dir}')
        pass
    return out_dir

def read_nd2(path:str, bundle_axes='yx', pos_limit=None):
    with nd.ND2_Reader(path,) as frames:
        logger.debug(frames.sizes)
        logger.debug(frames.metadata)
        frames.iter_axes = 'm'  # 't' is the default already
        frames.bundle_axes = bundle_axes  # when 'z' is available, this will be default
        for well in frames[:pos_limit]:
            yield well

def combine_nd2(*paths, out_folder):
    # get handlers to every file
    # iterate by 'm'
    # read first 'm's
    # stack them
    # save tif
    readers = [read_nd2(p) for p in paths]
    logger.info(f'Saving tifs to {os.path.join(out_folder, "Pos_XXX.tif")}')
    for i, images in tqdm(enumerate(zip(*readers))):
        time_series = np.array(images, dtype='uint16')
        logger.debug(time_series.shape)
        path = os.path.join(out_folder, f'Pos_{i:03d}.tif')
        imsave(path, time_series, imagej=True )
        logger.debug(f'saving to {path}')


def main():

    subname = 'Combined1'

    path = sys.argv[-1]
    logger.info(f'processing {path}')
    
    files = get_paths(path)
    logger.info(f'found {len(files)} datasets: \n{files}')

    conditions = get_conditions(files)
    logger.info(f'Found {len(conditions)}: \n{conditions}')

    inputs = combine_input_files(path, conditions)
    
    def process_condition(cond):
        logger.info(f'Condition: {cond}')
        out_folder = create_out_folder(path, cond, subname)
        combine_nd2(*inputs[cond]['inputs'], out_folder=out_folder)
        return True

    _ = list(map(process_condition, conditions))
    logger.info('Done processing')

    exit(0)

if __name__ == "__main__":
    main()


