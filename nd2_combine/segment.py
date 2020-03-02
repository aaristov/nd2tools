import cv2
import numpy as np
from skimage.measure import regionprops, label
from scipy.ndimage import gaussian_filter, binary_erosion
import matplotlib.pyplot as plt
import matplotlib
import logging

matplotlib.logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def findSpheroid(
    imCropped:np.ndarray,
    sigma:float = 5,
    erode:int = 3,
    threshold:float=0.5,
    max_ecc:float = 0.95,
    lim_major_axis_length:tuple=(100, 300),
    plot:bool=False
):

    """

    We find the spheroid by thresholding the intensity
    and area filling. Sph. must have a dark border around
    it.

    returns mask
    """


    result1, result2 = np.gradient(imCropped)
#     result2 = ndimage.sobel(imCropped, 0)


#     mask = _makeDiskMask(wellDiameter, wellDiameter-marginDistance-20, aspectRatio)
    grad = np.sqrt(result1 ** 2 + result2 ** 2)
    if plot:
        plt.imshow(grad)
        plt.show()

    toThresh = gaussian_filter(grad, sigma=sigma)

    imThresh = toThresh > np.max(toThresh) * threshold

    cnts, h = cv2.findContours(imThresh.astype('uint8'), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    mask = cv2.drawContours(imThresh.astype('uint8'), cnts, -1, (255,255,255), thickness=cv2.FILLED)
    eroded_mask = binary_erosion(mask, structure=np.ones((erode, erode))).astype(mask.dtype)

    temp = eroded_mask

    imLabel = label(temp)
    logger.debug(f'found {imLabel.max()} regions')
    if plot:
        plt.imshow(imLabel)
        plt.show()

    for i, region in enumerate(regionprops(imLabel)):
        logger.debug(f'filtering region {i}')

        if region.eccentricity > max_ecc:
        #check it is inside or outside
            logger.debug(f'eccentricity {region.eccentricity} > {max_ecc}')

            temp[imLabel == region.label] = 0
            #region given same value as sph. border

        if region.major_axis_length < lim_major_axis_length[0] or region.major_axis_length > lim_major_axis_length[1]:
            logger.debug(f'major_axis_length {region.major_axis_length} outside limits {lim_major_axis_length}')
            temp[imLabel == region.label] = 0

    if plot:
        plt.imshow(temp)
        plt.show()

    return temp


def get_props(mask:np.ndarray, **kwargs):
    lab = label(mask)
    # assert lab.max() == 1, f'number of segments is {lab.max()}'
    reg = regionprops(lab)
    return [{'area': r.area, 'eccentricity': r.eccentricity, 'major_axis_length': r.major_axis_length, **kwargs} for r in reg]