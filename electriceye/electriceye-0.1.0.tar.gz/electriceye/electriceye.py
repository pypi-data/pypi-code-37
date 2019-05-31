"""
electiceye

Module to compare images
"""
from skimage.measure import compare_ssim
import cv2
import imutils


def image_diff(path_a, path_b):
    """
    Returns the diffferences of two images based on
    the mean structural similarity index between them.

    Prameters
    ---------
    path_a, path_b : ndarray
        Image.


    Returns
    ---------
    mssim : float
        Represetns the structural similarity index
        between the two input imagess. This value can
        fall into the range [-1, 1] with a value of one
        being a perfect match.

    S : ndarray
        The full SSIM image.
    """
    img_a = cv2.imread(path_a, cv2.CV_8UC1)
    img_b = cv2.imread(path_b, cv2.CV_8UC1)

    (mssim, full_ssim) = compare_ssim(img_a,
                                      img_b,
                                      multichannel=True,
                                      full=True)
    diff = (full_ssim * 255).astype("uint8")
    gen_diff_img(img_a, img_b, diff)


    return {
        "mssim": mssim,
        "diff_img": img_b
    }


def to_gray(img):
    """
    Retruns the image taken as agrument but in a gray scale
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def show(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def gen_diff_img(img_a, img_b, full_ssim):
    thresh = cv2.threshold(full_ssim,
                           0,
                           255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[
                               1
                           ]
    cnts = cv2.findContours(thresh.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    red = (0, 0, 255)
    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(img_a, (x, y), (x + w, y + h), red, 2)
        cv2.rectangle(img_b, (x, y), (x + w, y + h), red, 2)
