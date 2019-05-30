import numpy as np

def flip(img, axis = 0) -> np.ndarray:
    """
    Method flips the image around either vertically (over horizontal axis = 0),
    or horizontally (over vertical axis = 1).

    :param axis: int(0/1). Flip the image vertically (over horizontal axis = 0) or vertically (over vertical axis = 1)
    :return: np.ndarray
    """
    img_cp = img.copy()

    if axis == 0:
        img_cp = np.flip(img_cp, axis = 0)
    if axis == 1:
        img_cp = np.flip(img_cp, axis = 1)

    return img_cp
