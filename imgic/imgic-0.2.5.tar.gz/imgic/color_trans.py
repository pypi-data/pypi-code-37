import numpy as np

def channelshuffle(img) -> np.ndarray:
    """
    Method randomly shuffles image's channels (swaps them places).

    :return: np.ndarray
    """
    img_cp = img.copy()

    img_cp = img_cp[:, :, np.random.permutation(3)]

    return img_cp


def colorjitter(img, channel, a, add_brightness = 0) -> np.ndarray:
    """
    Method increases intensity of the selected channel by parameter alpha and optionally
    increases/decreases its brightness.

    :param channel: int(0 <= channel < 3) - selected channel to jitter (0 = R, 1 = G, 2 = B).
    :param a: float(-1 <= alpha <= 1) - the amount of intensity to apply.
    :param add_brightness: float(-1 <= add_brightness <= 1) - the amount of brightness to add (default = 0).
    :return: np.ndarray
    """
    img_cp = img.copy()

    alpha = np.floor(a * 255)
    if alpha > 0:
        img_cp[:, :, channel] = np.where((255 - img_cp[:, :, channel]) < alpha, 255,
                                             img_cp[:, :, channel] + alpha)
    if alpha < 0:
        img_cp[:, :, channel] = np.where((255 + img_cp[:, :, channel] + alpha) < 0, 0,
                                             img_cp[:, :, channel] + alpha)

    alpha_b = np.floor(add_brightness * 255)
    if alpha_b > 0:
        img_cp = np.where((255 - img_cp) < alpha_b, 255, img_cp + alpha_b)
    if alpha_b < 0:
        img_cp = np.where((255 + img_cp + alpha) < 0, 0, img_cp + alpha_b)
    img_cp = np.array(img_cp, dtype = np.uint8)

    return img_cp