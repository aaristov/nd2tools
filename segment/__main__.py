import sys
import os
import numpy as np
import pandas as pd
import segment
from nd2_combine import tools
from functools import partial
import logging
import click

logger = logging.getLogger(__name__)

@click.command()
@click.argument('path', type=click.File('r'), nargs=-1)#, help='one or several nd2 files')
@click.option(
    '--out_dir_suffix', '-o',
    type=click.Path(),
    default='',
    help='Where to save the preview png for segmentation. Default: filename without .nd2'
)
@click.option('--len_range_px', type=click.IntRange(), default=(50,500))

def main(path, out_dir_suffix, len_range_px):
    reader = tools.read_nd2(path)
    dirr = create_results_dir(path, suffix=out_dir_suffix)
    res = list(map(
        partial(process, dirr=dirr, lim_major_axis_length=len_range_px),
        tools.tqdm(reader)
    ))
    df = pd.DataFrame(res)
    csv_path = path.replace(".nd2", "_stats.csv")
    df.to_csv(csv_path)
    logger.info(f"Saved stats to {csv_path}")


def create_results_dir(nd2_path, suffix=""):
    dirr = nd2_path.replace(".nd2", suffix)
    try:
        os.mkdir(dirr)
        logger.info(f"Created {dirr}")
    except FileExistsError:
        logger.warning(f"{dirr} already exists")
    return dirr


def process(img, index=0, save="png", dirr=None, lim_major_axis_length=(50, 300)):
    index = img["well_index"]
    xy = img["well"]
    calibration_um = img["calibration_um"]
    shape = xy.shape
    crop = xy[
        shape[0] // 4 : shape[0] * 3 // 4, shape[1] // 4 : shape[1] * 3 // 4,
    ]

    logging.info(f"Processing {index} well")
    seg, fig = segment.findSpheroid(
        crop,
        threshold=0.3,
        erode=8,
        sigma=5,
        lim_major_axis_length=(50, 300),
        plot=1,
    )

    if save == "tif":
        stack = np.array([img["well"], seg], dtype="uint16")
        well = tools.Well(
            stack, order="cyx", calibration_um=calibration_um
        )
        well.save_tif(os.path.join(dirr, f"Pos_{index:03d}.tif"))
    if save == "png":
        fig.savefig(os.path.join(dirr, f"Pos_{index:03d}.png"))

    res = segment.get_props(seg, well_index=index)

    print(res)
    if len(res) > 1:
        res = res[np.argmax([a["area"] for a in res])]

        print(res)
        return res
    elif len(res) == 1:
        return res[0]
    else:
        return {"well_index": index}


if __name__ == "__main__":
    args = sys.argv
    path = args[-1]

    main(path)
