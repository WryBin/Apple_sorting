# -*-coding:utf-8-*-

import cv2
import math
import numpy as np

import imgprocessing


def apple_size(img_in, binary_img, size_method, return_m):
    """ 1. Minimum external rectangle  2. Maximum inner circle"""
    # Get the contours
    contours, __ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

    pt2mm = 3.3  # point to mm, conversion of units

    if size_method == 1:  # Minimum external rectangle

        apple_size_img = img_in.copy()

        rect = cv2.minAreaRect(contours[0])

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        if return_m == 1:

            cx, cy = rect[0]
            cv2.drawContours(apple_size_img, [box], 0, (0, 0, 255), 2)
            cv2.circle(apple_size_img, (np.int32(cx), np.int32(cy)), 2, (255, 0, 0), 2, 8, 0)

            return apple_size_img

        elif return_m == 2:

            side1 = box[0] - box[1]
            side2 = box[0] - box[3]
            side = np.zeros(2)
            side[0] = math.hypot(side1[0], side1[1])
            side[1] = math.hypot(side2[0], side2[1])

            diameter = np.max(side)/pt2mm
            diameter = diameter - (diameter - 80) * 0.3
            return diameter

    elif size_method == 2:  # Maximum inner circle

        circle_img = binary_img.copy()

        # Calculate the distances to the contour
        raw_dist = np.empty(circle_img.shape, dtype=np.float32)
        for ic in range(circle_img.shape[0]):
            for jc in range(circle_img.shape[1]):
                raw_dist[ic, jc] = cv2.pointPolygonTest(contours[0], (jc, ic), True)

        # Get the center and the radius of the inner circle.
        __, maxval, __, max_dist_pt = cv2.minMaxLoc(raw_dist)
        maxval = abs(maxval)

        if return_m == 1:

            cv2.circle(img_in, max_dist_pt, np.int(maxval), (0, 255, 0), 2, cv2.LINE_8, 0)
            return img_in

        elif return_m == 2:

            diameter = (maxval * 2)/pt2mm
            diameter = diameter - (diameter - 80) * 0.3
            return diameter

    elif size_method == 3:  # Minimum outer circle

        circle_img = img_in.copy()

        (x, y), radius = cv2.minEnclosingCircle(contours[0])

        center = (int(x), int(y))
        radius = int(radius)

        if return_m == 1:

            cv2.circle(circle_img, center, radius, (255, 255, 0), 2)
            return circle_img

        elif return_m == 2:

            diameter = (radius * 2)/pt2mm
            diameter = diameter - (diameter - 80) * 0.3
            return diameter


def apple_roundness(binary_img):
    """ Roundness calculating"""

    contours, __ = cv2.findContours(binary_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

    area = cv2.contourArea(contours[0])
    arclen = cv2.arcLength(contours[0], True)

    # print("area", area)
    # print("arclen", arclen)

    roundness = (4 * np.pi * area)/(arclen * arclen)

    return roundness


def apple_coloring_rate(img_in, color_rate_method, binary_img, return_m):
    """ 1. V_ExR - V_ExG 2. HSV"""

    if color_rate_method == 1:  # V_ExR-V_ExG

        img_in[:, :, 0] = cv2.equalizeHist(img_in[:, :, 0])
        img_in[:, :, 1] = cv2.equalizeHist(img_in[:, :, 1])
        img_in[:, :, 2] = cv2.equalizeHist(img_in[:, :, 2])

        b = img_in[:, :, 0].astype(np.int16)
        g = img_in[:, :, 1].astype(np.int16)
        r = img_in[:, :, 2].astype(np.int16)

        v_exr = r * 2 - g - b
        v_exg = g * 1.4 - r

        red_area = v_exr - v_exg
        red_area[red_area > 0] = 255
        red_area[red_area < 0] = 0
        red_area = 255 - red_area
        red_area = red_area.astype(np.uint8)

        # cv2.imshow("red_area", red_area)
        return red_area

    if color_rate_method == 2:  # HSV

        img_hsv = cv2.cvtColor(img_in, cv2.COLOR_BGR2HSV)

        img_hsv = img_hsv[:, :, 1]

        if return_m == 1:

            img_hsv[img_hsv < 50] = 0
            img_hsv[img_hsv >= 50] = 255

            img_hsv = 255 - img_hsv

            return img_hsv

        if return_m == 2:

            img_hsv[img_hsv < 50] = 0
            img_hsv[img_hsv >= 50] = 1

            contours, __ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours.sort(key=lambda c: cv2.contourArea(c), reverse=True)

            area = cv2.contourArea(contours[0])

            red_rate = np.sum(img_hsv) / area

            if red_rate > 1:
                red_rate = 1.00

            return red_rate

