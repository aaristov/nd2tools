import cv2
import numpy as np
from skimage.measure import regionprops, label
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib
import logging

matplotlib.logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

def findSpheroid(
    imCropped:np.ndarray,
    sigma:float = 5,
    threshold:float=0.5,
    max_ecc:float = 0.95,
    max_major_axis_length=300,
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
    temp = cv2.drawContours(imThresh.astype('uint8'), cnts, -1, (255,255,255), thickness=cv2.FILLED)

    imLabel = label(temp)
    logger.debug(f'found {imLabel.max()} regions')
    if plot:
        plt.imshow(imLabel)
        plt.show()

    for i, region in enumerate(regionprops(imLabel)):
        logger.debug(f'filtering region {i}')

        if region.eccentricity > max_ecc:
        #check it is inside or outside
            logger.debug(f'eccentricity {region.eccentricity} > 0.8')

            temp[imLabel == region.label] = 0
            #region given same value as sph. border

        if region.major_axis_length > max_major_axis_length:
            logger.debug(f'major_axis_length {region.major_axis_length} > max_major_axis_length {max_major_axis_length}')
            temp[imLabel == region.label] = 0

    if plot:
        plt.imshow(temp)
        plt.show()

    return temp


def get_props(mask:np.ndarray):
    lab = label(mask)
    # assert lab.max() == 1, f'number of segments is {lab.max()}'
    reg = regionprops(lab)
    return [{'area': r.area, 'eccentricity': r.eccentricity, 'major_axis_length': r.major_axis_length} for r in reg]