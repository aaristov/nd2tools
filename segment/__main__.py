import sys
import os
import numpy as np
import pandas as pd
from segment import seg
from nd2_combine import tools
from functools import partial
import logging
import click
from multiprocessing import Pool, cpu_count
from glob import glob

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('path',  nargs=-1)#, help='one or several nd2 files')
@click.option(
    '--out_dir_suffix', '-o',
    # type=click.Path(),
    default='_segment',
    show_default=True,
    help='Where to save the preview png for segmentation.'
)
@click.option('--len_range_px', '-l', type=(int, int), default=(50,500), show_default=True, help='min, max length of major axis in pixels')
@click.option('--log', type=str, default='info', show_default=True, help='Logging level')

def main(path:list=[], out_dir_suffix:str='', len_range_px:tuple=(50,500), log='info'):

    logging.basicConfig(level=getattr(logging, log.upper()))
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log.upper()))
    
    flist = check_paths(path)
    logger.info(f'Total {len(flist)} files')

    fun = partial(process, out_dir_suffix=out_dir_suffix, len_range_px=len_range_px, logger=logger)
    _ = list(map(fun, flist))
    return True

def check_paths(paths:list):
    flist = []
    for p in paths:
        if os.path.exists(p):
            flist.append(p)
        else:
            pp = glob(p)
            [flist.append(ppp) for ppp in check_paths(pp)]
    return flist


def process(path:str='', out_dir_suffix:str='', len_range_px:tuple=(50,500), logger=logging):
    logger.info(f'Processing {path}')
    logger.debug(f'len_range_px = {len_range_px}')
    reader = tools.read_nd2(path)
    dirr = create_results_dir(path, suffix=out_dir_suffix)

    try:
        p = Pool(processes=(c := cpu_count()))
        logger.info(f'Processing using pool of {c} workers')
        res = p.map(
            partial(seg.crop_and_segment, dirr=dirr, lim_major_axis_length=len_range_px, print_dot=True),
            reader
        )
    except Exception as e:
        logger.error(e, 'fall back to serial execution')
        res = list(map(
            partial(seg.crop_and_segment, dirr=dirr, lim_major_axis_length=len_range_px),
            tools.tqdm(reader, desc='Well')
        ))
    df = pd.DataFrame(res)
    csv_path = path.replace(".nd2", "_stats.csv")
    df.to_csv(csv_path)
    logger.info(f"Saved stats to {csv_path}")
    return True


def create_results_dir(nd2_path, suffix=""):
    dirr = nd2_path.replace(".nd2", suffix)
    try:
        os.mkdir(dirr)
        logger.info(f"Created {dirr}")
    except FileExistsError:
        logger.warning(f"{dirr} already exists")
    return dirr



if __name__ == "__main__":
    main()
