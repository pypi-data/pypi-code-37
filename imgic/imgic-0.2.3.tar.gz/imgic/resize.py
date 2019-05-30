import numpy as np

def resize(img, a=0, height=0, width=0) -> np.ndarray:
    """
    Method resizes image to either fixed height/width or to size equal to
    proportion of original size a.

    :param a: float(0 < a) - proportional resizing parameter alpha (returned dims = a * original dims)
    :param height: int(0 < height) - height of resized image (in px)
    :param width: int(0 < width) - width of resized image (in px)
    :return: np.ndarray
    """

    img_cp = img.copy()

    rowlen = np.round(img_cp.shape[0] * (a)) if (height == 0) & (width == 0) else height
    collen = np.round(img_cp.shape[1] * (a)) if (height == 0) & (width == 0) else width

    img_cp = img_cp[np.linspace(0, img_cp.shape[0] - 1, rowlen, dtype = np.uint16), :, :]
    img_cp = img_cp[:, np.linspace(0, img_cp.shape[1] - 1, collen, dtype = np.uint16), :]

    return img_cp