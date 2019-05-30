import numpy as np
import .resize as resize
import .blur as blur
import .color_trans as color_trans
import .crop as crop
import .dropout as dropout
import .flip as flip
import .combine as combine


class Img:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.shape = self.image.shape

    def __repr__(self):
        return f'Image object of {self.shape[0]}x{self.shape[1]}'

    def crop(self, px = [0, 0, 0, 0], pc = [0, 0, 0, 0], tp_l = [], bt_r = [], keep_size = 0) -> 'Img':
        """
        This method crops the image, based either on an input list of the amount of pixels
        to crop (top/right/bottom/left), percentage of pixels to crop, or two coordinates:
        top_left, and bottom_right corner.

        :param px: list(top, right, bottom, left) - number of pixels to crop at each side.
        :param pc: list(top, right, bottom, left) - percentage of pixels to crop at each side.
        :param tp_l: list(row, column) - coordinate of top-left corner for coordinate based cropping.
        :param bt_r: list(row, column) - coordinate of bottom-right corner for coordinate based cropping.
        :param keep_size: int(1/0) - resize cropped image to original size (default = 0).
        :return: Img class instance
        """
        self.image = crop.crop(self.image, px, pc, tp_l, bt_r, keep_size)
        self.shape = self.image.shape
        return self

    def fixed_crop(self, height = 150, width = 150, v_pos = "center", h_pos = "center", keep_size=0) -> 'Img':
        """
        Method crops the image to selected height/width, at the specific
        location of the image along horizontal/vertical axes (center, top/bottom-left/right, random).

        :param height: int() - crop to height (in px)
        :param width:  int() - crop to width (in px)
        :param v_pos: str("center"/"top"/"bottom"/"random") - crops image at selected vertical location
        :param h_pos: str("center"/"left"/"right"/"bottom") - crops image at selected horizontal location
        :param keep_size: keep_size: int(1/0) - resize cropped image to original size (default = 0)
        :return: Img class instance
        """
        self.image = crop.fixed_crop(self.image, height, width, v_pos, h_pos, keep_size)
        self.shape = self.image.shape
        return self

    def flip(self, axis = 0) -> 'Img':
        """
        Method flips the image around either vertically (over horizontal axis = 0),
        or horizontally (over vertical axis = 1).

        :param axis: int(0/1). Flip the image vertically (over horizontal axis = 0) or vertically (over vertical axis = 1)
        :return: Img class instance
        """
        self.image = flip.flip(self.image, axis)
        self.shape = self.image.shape
        return self

    def blur(self, a = 1) -> 'Img':
        """
        Method applies Gaussian blurring to the input, with the strength alpha. The method
        maintains the original size of the object, but inserts a black border.

        :param a: int(1 <= a < inf) - parameter to repeat the blurring a times. Strengthens the effect.
        :return: Img class instance
        """
        self.image = blur.blur(self.image, a)
        self.shape = self.image.shape
        return self

    def dropout(self, a = 0.5) -> 'Img':
        """
        Method drops out the selected fraction of pixels from the input image (replaces
        with black pixels).

        :param a: float(0 <= a <= 1) - the fraction of pixels to remove from the image (default = 0.5 = 50%)
        :return: Img class instance
        """
        self.image = dropout.dropous(self.image, a)
        self.shape = self.image.shape
        return self

    def channelshuffle(self) -> 'Img':
        """
        Method randomly shuffles image's channels (swaps them places).

        :return: Img class instance
        """
        self.image = color_trans.channelshuffle(self.image)
        self.shape = self.image.shape
        return self

    def colorjitter(self, channel, a, add_brightness=0) -> 'Img':
        """
        Method increases intensity of the selected channel by parameter alpha and optionally
        increases/decreases its brightness.

        :param channel: int(0 <= channel < 3) - selected channel to jitter (0 = R, 1 = G, 2 = B).
        :param a: float(-1 <= alpha <= 1) - the amount of intensity to apply.
        :param add_brightness: float(-1 <= add_brightness <= 1) - the amount of brightness to add (default = 0).
        :return: Img class instance
        """
        self.image = color_trans.colorjitter(self.image, channel, a, add_brightness)
        self.shape = self.image.shape
        return self

    def resize(self, a = 0, height = 0, width = 0) -> 'Img':
        """
        Method resizes image to either fixed height/width or to size equal to
        proportion of original size a.

        :param a: float(0 < a) - proportional resizing parameter alpha (returned dims = a * original dims)
        :param height: int(0 < height) - height of resized image (in px)
        :param width: int(0 < width) - width of resized image (in px)
        :return: Img class instance
        """
        self.image = resize.resize(self.image, a, height, width)
        self.shape = self.image.shape
        return self

    def combine(self, target_image, a = 0.5) -> 'Img':
        """
        Method combines the original image with a target image (rescaled to the same dims),
        using an opacity parameter a.

        :param target_image: Img() - an Img class instance type image, to combine with the first image.
        :param a: float(0 <= a <= 1) - opacity parameter (1 = original image only, 0 = target image only)
        :return: Img class instance
        """
        self.image = combine.combine(self.image, target_image.image, a)
        self.shape = self.image.shape
        return self
