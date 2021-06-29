# -*-coding:utf-8-*-

import cv2
import numpy as np

import imgprocessing as ip
import featuredetection as fd

from PIL import Image


def roi_get(img_in, roi_type, mask):
    """Get the region of interest"""

    if roi_type == 'apple':

        roi = cv2.bitwise_and(img_in, img_in,  mask=mask)
        return roi

    if roi_type == 'defection':
        pass


def main_processing(img):

    # img processing
    gray_img = ip.img_graying(img, 2)
    de_no_gray = ip.img_de_noising(gray_img, 5)
    de_no_BGR = ip.img_de_noising(img, 5)
    binary_img = ip.img_binarization(de_no_gray, 1)

    # apple feature detection
    diameter = fd.apple_size(de_no_BGR, binary_img, size_method=3, return_m=2)
    roundness = fd.apple_roundness(binary_img)
    red_rate = fd.apple_coloring_rate(roi_get(img, 'apple', binary_img), 2, binary_img, return_m=2)

    # make some changes
    diameter = int(diameter)
    roundness = int(round(roundness, 2) * 100)
    red_rate = int(round(red_rate, 2) * 100)

    # grade
    if diameter >= 70:
        diameter_grade = 1
    elif 70 > diameter >= 65:
        diameter_grade = 2
    else:
        diameter_grade = 3

    if roundness >= 88:
        roundness_grade = 0
    elif 88 > roundness >= 86:
        roundness_grade = 1
    elif 86 > roundness >= 84:
        roundness_grade = 2
    else:
        roundness_grade = 3

    if red_rate >= 90:
        red_rate_grade = 0
    elif 90 > red_rate >= 80:
        red_rate_grade = 1
    elif 80 > red_rate >= 55:
        red_rate_grade = 2
    else:
        red_rate_grade = 3

    grade = np.zeros(6)
    grade[0] = diameter
    grade[1] = diameter_grade
    grade[2] = roundness
    grade[3] = roundness_grade
    grade[4] = red_rate
    grade[5] = red_rate_grade

    img_out = np.zeros([129, 128, 3])

    img = Image.fromarray(img)
    img = img.resize([128, 128], Image.ANTIALIAS)
    img = np.array(img)

    img_out[0, 0:6, 0] = grade
    img_out[1:, :, :] = img

    img_out = img_out.astype(np.uint8)

    return img_out


if __name__ == "__main__":

    filename = '/home/jon/Graduation_project/imgtest.jpg'
    img_name = cv2.imread(filename)

    main_processing(img_name)
