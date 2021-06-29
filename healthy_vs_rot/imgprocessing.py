# -*-coding:utf-8-*-

import cv2
import numpy as np


def img_graying(img_in, gray_method):
    """1.Direct call to function 2.The maximum value method 3.mean method 4.Weighted mean method"""

    if gray_method == 1:  # Direct call to function: cv2.cvtColor for image grayscale processing.
        gray = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
    # @1
    # gray = img_in.copy()
    # img_in_shape = img_in.shape
    # for i in range(img_in_shape[0]):
    #     for j in range(img_in_shape[1]):
    #         if gray_method == 2:  # The maximum value method.
    #             gray[i, j] = max(img_in[i, j][0], img_in[i, j][1], img_in[i, j][2])
    #         if gray_method == 3:
    #             # @1 gray[i, j] = np.mean([img_in[i, j][0], img_in[i, j][1], img_in[i, j][2]])
    #             gray[i, j] = (img_in[i, j][0] + img_in[i, j][1] + img_in[i, j][2])/3
    #         if gray_method == 4:  # Weighted mean method:
    #             weight = [0.11, 0.59, 0.3]  # The weight is determined according to the sensitivity of human eyes.
    #             gray[i, j] = np.average([img_in[i, j][0], img_in[i, j][1], img_in[i, j][2]], weights=weight)
    #           # @1 gray[i, j] = img_in[i, j][0] * 0.11 + img_in[i, j][1] * 0.59 + img_in[i, j][2] * 0.3
    # return gray
    elif gray_method == 2:  # The maximum value method
        gray = np.max(img_in, axis=2)

    elif gray_method == 3:  # Mean method
        gray = np.mean(img_in, axis=2).astype(np.uint8)

    elif gray_method == 4:  # Weighted mean method:
        weight = [0.11, 0.59, 0.3]
        gray = np.average(img_in, axis=2, weights=weight).astype(np.uint8)

    else:
        gray = img_in.copy()
        print("Img grayscale error")

    return gray


def img_de_noising(img_in, de_no_method):
    """
    1. MeanBlur 2. GaussianBlur 3. GaussianBlur 4. cv2.fastNlMeansDenoising
    EPF 5. bilateralFilter
    """

    if de_no_method == 1:  # MeanBlur
        de_no = cv2.blur(img_in, (5, 5))

    elif de_no_method == 2:  # MedianBlur
        de_no = cv2.medianBlur(img_in, 5)

    elif de_no_method == 3:  # GaussianBlur
        de_no = cv2.GaussianBlur(img_in, (5, 5), 0)

    elif de_no_method == 4:  # fastNlMeansDenoising
        de_no = cv2.fastNlMeansDenoising(img_in)

    elif de_no_method == 5:  # bilateralFilter
        de_no = cv2.bilateralFilter(img_in, 10, 100, 0)

    else:
        de_no = img_in
        print("de_no error")

    return de_no


def img_edge(img_in, edge_method):
    """1.Canny"""

    if edge_method == 1:
        edge = cv2.Canny(img_in, 50, 200)

    else:
        edge = img_in
        print("edge error")

    return edge


def img_binarization(img_in, binary_method):
    """1. threshold"""

    if binary_method == 1:
        # t, binary = cv2.threshold(img_in, 50, 255, 0)
        t, binary = cv2.threshold(img_in, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    elif binary_method == 2:
        t, binary = cv2.threshold(img_in, 70, 255, cv2.THRESH_BINARY)

    # elif binary_method == 3:
        # binary = cv2.adaptiveThreshold(img_in, 255, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY, 11, 2)

    else:
        binary = img_in
        print("binary error")

    return binary
