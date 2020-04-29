from nd2tif import read, save
import sys
import os
import logging
import click
from functools import partial
from multiprocessing import Pool, cpu_count

logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)

@click.command()
@click.argument('path',  nargs=1)#, help='one or several nd2 files')
@click.option(
    '--bin', '-b',
    type=int,
    default=4,
    show_default=True,
    help='Image binning'
)
@click.option(
    '--to_8bits',
    is_flag=True,
    help='convert to 8 bits'
)
@click.option(
    '--log', type=str, default='info',
    show_default=True, help='Logging level'
)
@click.option(
    '--start', '-s', type=click.IntRange(0,1),
    default=0, show_default=True,
    help='Start numbering from 000 or 001'
)
@click.option(
    '--prefix', '-p', type=str,
    default='Pos_', show_default=True,
    help='Prefix for tif files'
)
@click.option(
    '--cpu', '-c', type=int,
    default=1, show_default=True,
    help='Number of CPU'
)

def main(path:str='', bin:int=4, to_8bits:bool=True, log='info', start=0, prefix='Pos_', cpu=1):
    logger.setLevel(getattr(logging, log.upper()))
    if not os.path.exists(path) or not path.endswith(".nd2"):
        logger.error("Provide valid .nd2 path")
        return False

    reader = read.nd2(path, pos_limit=None)

    folder = path.replace(".nd2", f"_binned_{bin}x{bin}_tifs")

    try:
        os.mkdir(folder)
        logger.info(f'Created new folder {folder}')
    except FileExistsError:
        logger.warning(f'Folder already exists {folder}')

    fun = partial(process, bin=bin, to_8bits=to_8bits, folder=folder,
                  prefix=prefix, start=start)
    iterator = enumerate(reader)

    if cpu > 1:
        try:
            p = Pool(processes=(n_cpu := min([cpu, cpu_count()])))
            logger.info(f'Running {n_cpu} workers')
            out = p.map(fun, iterator)
        except Exception as e:
            logging.error(e, 'Fall bask to map')
            out = list(map(fun, iterator))
    else:
        out = list(map(fun, iterator))
    return True

def process(i_well:tuple, bin, to_8bits, folder, prefix, start):
    i, well = i_well
    if bin > 1:
        ds_well = well.downscale(bin)
    if to_8bits:
        ds_well = ds_well.to_8bits()
    name = os.path.join(folder, f"{prefix}{i+start:03d}.tif")
    save.tiff(name, ds_well.array)
    return True

if __name__ == "__main__":

    main()
