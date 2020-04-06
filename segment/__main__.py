import sys
import os
import numpy as np
import pandas as pd
import segment
from nd2_combine import tools
from functools import partial
import logging
import click

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('path',  nargs=-1)#, help='one or several nd2 files')
@click.option(
    '--out_dir_suffix', '-o',
    # type=click.Path(),
    default='',
    help='Where to save the preview png for segmentation. Default: filename without .nd2'
)
@click.option('--len_range_px', '-l', type=(int, int), default=(50,500), show_default=True)
@click.option('--log', type=str, default='info', show_default=True)

def main(path:list=[], out_dir_suffix:str='', len_range_px:tuple=(50,500), log='info'):

    logging.basicConfig(level=getattr(logging, log.upper()))
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log.upper()))
    logger.info(f'Total {len(path)} files')
    fun = partial(process, out_dir_suffix=out_dir_suffix, len_range_px=len_range_px, logger=logger)
    _ = list(map(fun, path))
    return True

def process(path:str='', out_dir_suffix:str='', len_range_px:tuple=(50,500), logger=logging):
    logger.info(f'Processing {path}')
    logger.debug(f'len_range_px = {len_range_px}')
    reader = tools.read_nd2(path)
    dirr = create_results_dir(path, suffix=out_dir_suffix)
    res = list(map(
        partial(crop_and_segment, dirr=dirr, lim_major_axis_length=len_range_px),
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


def crop_and_segment(img, save="png", dirr='.', lim_major_axis_length=(50, 300)):
    index = img["well_index"]
    xy = img["well"]
    calibration_um = img["calibration_um"]
    shape = xy.shape
    crop = xy[
        shape[0] // 4 : shape[0] * 3 // 4, shape[1] // 4 : shape[1] * 3 // 4,
    ]

    logging.debug(f"Processing {index} well")
    seg, fig = segment.findSpheroid(
        crop,
        threshold=0.3,
        erode=8,
        sigma=5,
        lim_major_axis_length=(50, 700),
        plot=1,
    )

    if save == "tif":
        stack = np.array([img["well"], seg], dtype="uint16")
        well = tools.Well(
            stack, order="cyx", calibration_um=calibration_um
        )
        well.save_tif(os.path.join(dirr, f"Pos_{index:03d}.tif"))
    if save == "png":
        fig_path = os.path.join(dirr, f"Pos_{index:03d}.png")
        fig.savefig(fig_path)
        logger.debug(f'Saved {fig_path}')

    res = segment.get_props(seg, well_index=index)

    logger.debug(res)
    if len(res) > 1:
        res = res[np.argmax([a["area"] for a in res])]

        logger.debug(res)
        return res
    elif len(res) == 1:
        return res[0]
    else:
        return {"well_index": index}


if __name__ == "__main__":
    main()
