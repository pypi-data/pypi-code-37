import numpy as np

def dropout(img, a = 0.5) -> np.ndarray:
    """
    Method drops out the selected fraction of pixels from the input image (replaces
    with black pixels).

    :param a: float(0 <= a <= 1) - the fraction of pixels to remove from the image (default = 0.5 = 50%)
    :return: np.ndarray
    """
    img_cp = img.copy()

    img_cp[np.random.choice([0, 1], size = img_cp.shape[0:2],
                                p = [1 - a, a]).astype(np.bool)] = [0, 0, 0]

    return img_cp