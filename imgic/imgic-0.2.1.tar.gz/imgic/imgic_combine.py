import numpy as np
from imgic_resize import resize

def combine(img, target_image, a=0.5) -> np.ndarray:
    """
    Method combines the original image with a target image (rescaled to the same dims),
    using an opacity parameter a.

    :param target_image: Img() - an Img class instance type image, to combine with the first image.
    :param a: float(0 <= a <= 1) - opacity parameter (1 = original image only, 0 = target image only)
    :return: np.ndarray
    """
    img_cp = img.copy()

    if img_cp.shape != target_image.shape:
        target_image = resize(target_image, height = img_cp.shape[0], width = img_cp.shape[1])

    img_cp = np.array(target_image * (1 - a), dtype = np.uint16) + \
                 np.array(img_cp * a, dtype = np.uint16)
    return img_cp
