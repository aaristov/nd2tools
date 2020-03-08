import numpy as np
import pims_nd2 as nd
import pandas as pd
import seaborn as sns
import json
import logging
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, binary_erosion, binary_fill_holes, label, measurements
from skimage.measure import regionprops, regionprops_table


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_intensity_table(
    labelled_mask: np.ndarray,
    intensity_image_sequence: np.ndarray,
    plot: bool = True
):
    assert (iis := intensity_image_sequence).ndim == 3, (
        f'expected 3D stack for intensity, got shape {iis.shape}'
    )
    df = pd.DataFrame(columns=['time', 'label', 'max_intensity', 'mean_intensity'])

    for t in range(len(iis)):
        dict_li = regionprops_table(
            labelled_mask,
            intensity_image=iis[t],
            properties=['label', 'max_intensity', 'mean_intensity']
        )
        dict_lit = {'time': [t]*len(dict_li['label']), **dict_li}
        df1 = pd.DataFrame.from_dict(dict_lit)
        df = pd.concat([df, df1])

    if plot:
        plot_intensity_vs_time(df)
    return df


def filter_table_by_min_intensity(table:pd.DataFrame, time:int, min_intensity:float):
    '''
    Returns rows which at time `time` have `mean_intensity` > `min_intensity`
    '''
    return table[table[table.time == time].mean_intensity > min_intensity]


def filter_table_by_max_intensity(table:pd.DataFrame, time:int, max_intensity:float):
    '''
    Returns rows which at time `time` have `mean_intensity` < `max_intensity`
    '''
    return table[table[table.time == time].mean_intensity < max_intensity]


def read_stitched_nd2(path: str, bundle="zyx", channel=0, time_limit=None):
    """
    Reads nd2 with bundle, channel
    Yields one timepoint at a time.
    """

    with nd.ND2_Reader(path,) as frames:
        logger.info(frames.sizes)
        # logger.info(frames.calibration)
        # logger.info(frames.calibrationZ)

        # json.dump(frames.metadata, open(path.replace('.nd2','_meta.json'), 'w'), default=repr)
        frames.iter_axes = "t"
        frames.default_coords["c"] = channel
        frames.bundle_axes = bundle
        for zyx in frames[:time_limit]:
            yield zyx


def get_mask(
    bf_stack,
    use_time: int = 0,
    erode: int = 10,
    # area_lim : tuple = (None, None),
    # eccentricity_lim: tuple = (None, None),
    plot=True
) -> np.ndarray:
    '''
    Creates a labelled mask using first image from bf stack
    '''

    bf = bf_stack[use_time]

    mask = _detect_wells(bf, erode=erode)
    labels, n_labels = label(mask)
    regions = regionprops(labels, intensity_image=None)
    print(len(regions), ' regions')

    areas = np.array([r.area for r in regions])
    mean_areas = areas.mean()
    std_areas = areas.std()
    area_lim = (mean_areas - 1*std_areas, mean_areas + 1*std_areas)

    bad_regions = list(filter(lambda r: r.area < area_lim[0] or r.area > area_lim[1] or r.eccentricity > 0.7, regions))
    print(len(bad_regions), ' bad regions')

    bad_mask = np.max([labels == br.label for br in bad_regions], axis=0)


    good_mask = mask.copy()
    good_mask[bad_mask] = 0

    good_labels, n  = label(good_mask)

    print(f'{n} good regions')

    if plot:

        show(bf, vmax=bf.max())
        plt.title('input')
        plt.show()

        h, bins, _ = plt.hist([r.area for r in regions], bins=30)
        plt.vlines(mean_areas, ymin=0, ymax=h.max())
        plt.vlines(area_lim[0], ymin=0, ymax=h.max() / 3)
        plt.vlines(area_lim[1], ymin=0, ymax=h.max() / 3)
        plt.title('area')
        plt.show()

        plt.hist([r.eccentricity for r in regions], bins=30)
        plt.title('eccentricit  y')
        plt.show()
        
        show(bad_mask)
        plt.title('bad regions')
        plt.show()
        

        show(good_mask)
        plt.title('good mask')
        plt.show()

        show(good_labels)
        plt.title('good labels')
        plt.show()

    return good_labels


def _detect_wells(bf: np.ndarray, thr=0.1, sigma=2, erode=5, plot=False):
    '''
    Return mask of wells
    '''
    grad = get_2d_gradient(bf)
    sm_grad = gaussian_filter(grad, sigma)
    mask = sm_grad > sm_grad.max() * thr
    filled_mask = binary_erosion(
        binary_fill_holes(mask),
        structure=np.ones((erode, erode))
    )

    if plot:
        [show(b) for b in [grad, sm_grad, mask, filled_mask]]

    return filled_mask


def get_2d_gradient(xy):
    gx, gy = np.gradient(xy)
    return np.sqrt(gx ** 2 + gy ** 2)


def show(grad, **kwargs):
    plt.figure(figsize=(15, 10))
    plt.imshow(grad, cmap='gray', **kwargs)


def plot_intensity_vs_time(
    table: pd.DataFrame, x='time', y='mean_intensity', size=1, **kwargs
):
    ''' Swarm-plot '''
    plot = sns.swarmplot(data=table, x=x, y=y, size=size, **kwargs)
    return plot


def plot_intensity_line(
    table: pd.DataFrame, x='time', y='mean_intensity', **kwargs
):
    ''' Averaged line plot with confidence interval '''
    plot = sns.lineplot(data=table, x=x, y=y, ci='sd', **kwargs)
    return plot


def plot_intensity_raw_line(
    table: pd.DataFrame, x='time', y='mean_intensity', units='label', **kwargs
):
    ''' Plot every dataset in the series as a separate line '''
    plot = sns.lineplot(data=table, x=x, y=y, units=units, estimator=None, **kwargs)
    return plot