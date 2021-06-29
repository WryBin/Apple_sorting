# -*-coding:utf-8-*-

import cv2
import numpy as np
import matplotlib.pyplot as plt

import imgprocessing as ip
import featuredetection as fd


def roi_get(img_in, roi_type, mask):
    """Get the region of interest"""

    if roi_type == 'apple':

        roi = cv2.bitwise_and(img_in, img_in,  mask=mask)
        return roi

    if roi_type == 'defection':
        pass


def figure_show(img_in, fig_n):
    """Show the figures of processing test result"""

    import_img = "import_img" + str(ix) + str(iy)

    plt.figure(fig_n, figsize=(12, 16))
    plt.subplot(fig_y, fig_x, (ix - 1) * fig_x + iy)
    img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)
    plt.imshow(img_in)
    plt.title(import_img)
    plt.xticks([])
    plt.yticks([])


# filename = '/home/jon/Documents/python_files/Apple_sorting/Training_img/img1_1.jpg'
# img = cv2.imread(filename)

# gray_img = ip.img_graying(img, 2)
# de_no_gray = ip.img_de_noising(gray_img, 5)
# de_no_BGR = ip.img_de_noising(img, 4)
# edge_img = ip.img_edge(de_no_BGR, 1)
# binary_img = ip.img_binarization(de_no_gray, 2)
#
# apple_size_img = fd.apple_size(de_no_BGR, binary_img, size_method=3, return_m=1)
# fd.apple_roundness(binary_img)
# fd.apple_coloring_rate(roi_get(de_no_BGR, 'apple', binary_img), 2)
#
# cv2.imshow("img", img)
# cv2.imshow("binary_img", binary_img)
# cv2.imshow("apple_size_img", apple_size_img)


# The test of img processing method
# fig = plt.figure(figsize=(10, 8))
#
# for ia in np.arange(1, 5):
#     for ja in np.arange(1, 6):
#         gray_img = ip.img_graying(img, ia)
#         de_no_gray = ip.img_de_noising(gray_img, ja)
#         de_no_BGR = ip.img_de_noising(img, 4)
#         edge_img = ip.img_edge(de_no_BGR, 1)
#         binary_img = ip.img_binarization(de_no_gray, 2)
#
#         # apple_size_img = fd.apple_size(de_no_BGR, binary_img, size_method=3, return_m=1)
#         # fd.apple_size(de_no_BGR, binary_img, 1)
#         fd.apple_roundness(binary_img)
#         # fd.apple_coloring_rate(roi_get(de_no_BGR, 'apple', binary_img), 2)
#
#         title = "title" + str(ia) + str(ja)
#         plt.subplot(4, 5, (ia - 1) * 5 + ja)
#
#         gray_img = cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB)
#         binary_img = cv2.cvtColor(binary_img, cv2.COLOR_BGR2RGB)
#
#         # plt.imshow(gray_img)
#         # plt.imshow(edge_img)
#         # plt.imshow(apple_size_img)
#         plt.imshow(binary_img)
#         plt.title(title)
#         plt.xticks([])
#         plt.yticks([])
#
# plt.show()

diameter_array = np.array(0)
roundness_array = np.array(0)
red_rate_array = np.array(0)

# The number of pictures displayed
fig_x = 1
fig_y = 58

# Circle import.
for ix in np.arange(1, fig_y + 1):
    for iy in np.arange(1, fig_x + 1):

        filename = '/home/jon/Documents/python_files/Apple_sorting/Training_img/img{ix}_{iy}.jpg'.format(ix=ix, iy=iy)
        img = cv2.imread(filename)

        # img processing
        gray_img = ip.img_graying(img, 2)
        de_no_gray = ip.img_de_noising(gray_img, 5)
        de_no_BGR = ip.img_de_noising(img, 4)
        edge_img = ip.img_edge(de_no_BGR, 1)
        binary_img = ip.img_binarization(de_no_gray, 2)

        # diameter = fd.apple_size(de_no_BGR, binary_img, size_method=3, return_m=2)
        # diameter = int(diameter)
        # diameter_array = np.append(diameter_array, diameter)

        roundness = fd.apple_roundness(binary_img)
        roundness = round(roundness, 4)
        roundness_array = np.append(roundness_array, roundness)

        # red_rate = fd.apple_coloring_rate(roi_get(img, 'apple', binary_img), 2, binary_img, return_m=2)
        # red_rate = round(red_rate, 2)
        # red_rate_array = np.append(red_rate_array, red_rate)

        # apple feature detection
        # apple_size_img = fd.apple_size(de_no_BGR, binary_img, size_method=3, return_m=1)
        # fd.apple_roundness(binary_img)
        # red_area_img = fd.apple_coloring_rate(roi_get(img, 'apple', binary_img), 2, binary_img, return_m=1)

        # show the processing result
        # figure_show(img, 1)
        # figure_show(edge_img, 2)
        # figure_show(binary_img, 3)
        # figure_show(apple_size_img, 4)
        # figure_show(red_area_img, 5)

# print(diameter_array)
# print("min", min(diameter_array[1:59]))
# print("max", max(diameter_array[1:59]))

print(roundness_array)
print("min", min(roundness_array[1:59]))
print("max", max(roundness_array[1:59]))

# print(red_rate_array)
# print("min", min(red_rate_array[1:349]))
# print("max", max(red_rate_array[1:349]))

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
