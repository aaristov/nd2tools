import cv2
import numpy as np
from skimage.measure import regionprops, label
from scipy.ndimage import gaussian_filter, binary_erosion
import matplotlib.pyplot as plt
import matplotlib
from nd2_combine import tools
import os
import logging

matplotlib.logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def crop_and_segment(img, save="png", dirr='.', lim_major_axis_length=(50, 300)):
    index = img["well_index"]
    xy = img["well"]
    calibration_um = img["calibration_um"]
    shape = xy.shape
    crop = xy[
        shape[0] // 4 : shape[0] * 3 // 4, shape[1] // 4 : shape[1] * 3 // 4,
    ]

    logging.debug(f"Processing {index} well")
    seg, fig = find_spheroid(
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

    res = get_props(seg, well_index=index)

    logger.debug(res)
    if len(res) > 1:
        res = res[np.argmax([a["area"] for a in res])]

        logger.debug(res)
        return res
    elif len(res) == 1:
        return res[0]
    else:
        return {"well_index": index}


def find_spheroid(
    imCropped: np.ndarray,
    sigma: float = 5,
    erode: int = 3,
    threshold: float = 0.5,
    max_ecc: float = 0.95,
    lim_major_axis_length: tuple = (100, 400),
    plot: bool = False,
):

    """

    We find the spheroid by thresholding the intensity
    and area filling. Sph. must have a dark border around
    it.

    returns mask, of (mask, figure) if plot=True
    """

    result1, result2 = np.gradient(imCropped)
    grad = np.sqrt(result1 ** 2 + result2 ** 2)
    if plot:
        f, (ax1, ax2, ax3, ax4) = plt.subplots(
            1, 4, sharey=True, sharex=True, figsize=(10, 3)
        )
        ax1.imshow(imCropped, cmap="gray")
        ax1.set_title("raw")
        ax2.imshow(grad)
        ax2.set_title("grad")

    toThresh = gaussian_filter(grad, sigma=sigma)

    imThresh = toThresh > np.max(toThresh) * threshold

    cnts, h = cv2.findContours(
        imThresh.astype("uint8"), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    mask = cv2.drawContours(
        imThresh.astype("uint8"),
        cnts,
        -1,
        (255, 255, 255),
        thickness=cv2.FILLED,
    )
    eroded_mask = binary_erosion(
        mask, structure=np.ones((erode, erode))
    ).astype(mask.dtype)

    temp = eroded_mask

    imLabel = label(temp)
    logger.debug(f"found {imLabel.max()} regions")
    if plot:
        ax3.imshow(imLabel)
        ax3.set_title("all regions")

    for i, region in enumerate(regionprops(imLabel)):
        logger.debug(f"filtering region {i}")

        if region.eccentricity > max_ecc:
            # check it is inside or outside
            logger.debug(f"eccentricity {region.eccentricity} > {max_ecc}")

            temp[imLabel == region.label] = 0
            # region given same value as sph. border

        if (l := region.major_axis_length) < (lim := lim_major_axis_length)[
            0
        ] or l > lim[1]:
            logger.debug(f"major_axis_length {l} outside limits {lim}")
            temp[imLabel == region.label] = 0

    if plot:
        ax4.imshow(temp)
        ax4.set_title("Selected regions")
        return temp, f
    return temp


def get_props(mask: np.ndarray, **kwargs):
    lab = label(mask)
    # assert lab.max() == 1, f'number of segments is {lab.max()}'
    reg = regionprops(lab)
    return [
        {
            "area": r.area,
            "eccentricity": r.eccentricity,
            "major_axis_length": r.major_axis_length,
            **kwargs,
        }
        for r in reg
    ]
