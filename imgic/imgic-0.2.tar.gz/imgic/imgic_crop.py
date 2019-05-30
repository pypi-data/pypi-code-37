import numpy as np
from imgic_resize import resize


def crop(img, px=[0, 0, 0, 0], pc=[0, 0, 0, 0], tp_l = [], bt_r = [], keep_size = 0) -> np.ndarray:
    """
    This method crops the image, based either on an input list of the amount of pixels
    to crop (top/right/bottom/left), percentage of pixels to crop, or two coordinates:
    top_left, and bottom_right corner.

    :param px: list(top, right, bottom, left) - number of pixels to crop at each side.
    :param pc: list(top, right, bottom, left) - percentage of pixels to crop at each side.
    :param tp_l: list(row, column) - coordinate of top-left corner for coordinate based cropping.
    :param bt_r: list(row, column) - coordinate of bottom-right corner for coordinate based cropping.
    :param keep_size: int(1/0) - resize cropped image to original size (default = 0).
    :return: np.ndarray
    """
    img_cp = img.copy()

    if tp_l != []:
        px[0], px[3] = tp_l[0], tp_l[1]
    if bt_r != []:
        px[2], px[1] = bt_r[0], bt_r[1]
    if pc != [0, 0, 0, 0]:
        while len(pc) < 4:
            pc.append(0)
        px[0], px[1], px[2], px[3] = round(img_cp.shape[0] * pc[0]), round(img_cp.shape[0] * pc[1]), \
                                     round(img_cp.shape[1] * pc[2]), round(img_cp.shape[1] * pc[3])
    if px != [0, 0, 0, 0]:
        while len(px) < 4:
            px.append(0)
    img_cp = img_cp[0 + px[0]:img_cp.shape[0] - px[2],
                 0 + px[3]:img_cp.shape[1] - px[1], 0:3]

    if keep_size == 1:
        img_cp = resize(img_cp, height = img_cp.shape[0], width = img_cp.shape[1])

    return img_cp


def fixed_crop(img, height = 150, width = 150, v_pos = "center", h_pos = "center", keep_size = 0) -> np.ndarray:
    """
    Method crops the image to selected height/width, at the specific
    location of the image along horizontal/vertical axes (center, top/bottom-left/right, random).

    :param height: int() - crop to height (in px)
    :param width:  int() - crop to width (in px)
    :param v_pos: str("center"/"top"/"bottom"/"random") - crops image at selected vertical location
    :param h_pos: str("center"/"left"/"right"/"bottom") - crops image at selected horizontal location
    :param keep_size: keep_size: int(1/0) - resize cropped image to original size (default = 0)
    :return: np.ndarray
    """
    img_cp = img.copy()

    if v_pos == "center":
        margins = np.array([np.floor((img_cp.shape[0] - height) / 2),
                            np.floor((img_cp.shape[0] - (img_cp.shape[0] - height) / 2))],
                           dtype=np.uint16)
    if v_pos == "top":
        margins = np.array([0, height], dtype = np.uint16)
    if v_pos == "bottom":
        margins = np.array([img_cp.shape[0] - height, img_cp.image.shape[0]], dtype = np.uint16)
    if v_pos == "random":
        rand_gen = np.random.randint(0, img_cp.shape[0] - height)
        margins = np.array([rand_gen, rand_gen + width], dtype = np.uint16)

    if h_pos == "center":
        margins = np.append(margins, np.array([np.floor((img_cp.shape[1] - width) / 2),
                                               img_cp.shape[1] - np.ceil((img_cp.shape[1] - width) / 2)],
                                              dtype = np.uint16))
    if h_pos == "left":
        margins = np.append(margins, np.array([0, width], dtype = np.uint16))
    if h_pos == "right":
        margins = np.append(margins, np.array([img_cp.shape[1] - width, img_cp.shape[1]], dtype = np.uint16))
    if h_pos == "random":
        rand_gen = np.random.randint(0, img_cp.shape[1] - width)
        margins = np.append(margins, np.array([rand_gen, rand_gen + width], dtype = np.uint16))

    img_cp = img_cp[margins[0]:margins[1], margins[2]:margins[3], 0:3]

    if keep_size == 1:
        img_cp = resize(img_cp, height = img_cp.shape[0], width = img_cp.shape[1])

    return img_cp
