import numpy as np

def blur(img, a = 1) -> np.ndarray:
        """
        Method applies Gaussian blurring to the input, with the strength alpha. The method
        maintains the original size of the object, but inserts a black border.

        :param a: int(1 <= a < inf) - parameter to repeat the blurring a times. Strengthens the effect.
        :return: np.ndarray
        """

        kernel = np.array([[0.0625, 0.125, 0.00625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
        img_cp = img.copy()
        backup = img_cp.copy()

        for repeat in range(a):
            for channel in range(3):
                for row in range(0, img_cp.shape[0] - 2):
                    for col in range(0, img_cp.shape[1] - 2):
                        img_cp[row + 1, col + 1, channel] = np.floor(np.sum(backup[row:(row + 3),
                                                                                col:(col + 3), channel] * kernel))
        img_cp[[0, -1], :, :] = 0
        img_cp[: ,[0, -1], :] = 0

        return img_cp
