
import cv2
import numpy as np
import matplotlib.pyplot as plt

import imgprocessing as ip
import featuredetection as fd

plt.style.use('seaborn-whitegrid')


def figure_show(img_in, fig_n):
    """Show the figures of processing test result"""

    import_img = "import_img" + str(i)

    plt.figure(fig_n, figsize=(20, 12))
    plt.subplot(10, 6, i)
    img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)
    plt.imshow(img_in)
    plt.title(import_img, )
    plt.xticks([])
    plt.yticks([])


# The number of pictures displayed

fig_y = 58
diameter1_array = np.array(0)
diameter2_array = np.array(0)
diameter3_array = np.array(0)

# Circle import.
for i in np.arange(1, fig_y + 1):

    filename = '/home/jon/Documents/python_files/Apple_sorting/Training_img/img{i}_1.jpg'.format(i=i)
    img = cv2.imread(filename)

    # img processing
    gray_img = ip.img_graying(img, 2)
    de_no_gray = ip.img_de_noising(gray_img, 5)
    de_no_BGR = ip.img_de_noising(img, 4)
    edge_img = ip.img_edge(de_no_BGR, 1)
    binary_img = ip.img_binarization(de_no_gray, 2)

    # apple feature detection
    # apple_size_img = fd.apple_size(de_no_BGR, binary_img, size_method=1, return_m=1)

    diameter1 = fd.apple_size(de_no_BGR, binary_img, size_method=1, return_m=2)
    diameter1 = int(diameter1)
    diameter1_array = np.append(diameter1_array, diameter1)

    diameter2 = fd.apple_size(de_no_BGR, binary_img, size_method=2, return_m=2)
    diameter2 = int(diameter2)
    diameter2_array = np.append(diameter2_array, diameter2)

    diameter3 = fd.apple_size(de_no_BGR, binary_img, size_method=3, return_m=2)
    diameter3 = int(diameter3)
    diameter3_array = np.append(diameter3_array, diameter3)

    # fd.apple_roundness(binary_img)
    # red_area_img = fd.apple_coloring_rate(roi_get(img, 'apple', binary_img), 2)

    # show the processing result
    # figure_show(img, 1)
    # figure_show(edge_img, 2)
    # figure_show(binary_img, 3)
    # figure_show(apple_size_img, 4)
    # figure_show(red_area_img, 5)

    # feature detection for SVM
    # roi_get(de_no_BGR, 'defection')


fig = plt.figure()

x = np.arange(1, 59)
y = np.array([78, 81, 77, 86, 82, 79, 80, 82, 87, 84, 78, 83, 90, 84, 79, 74, 80, 83, 76, 85,
             84, 84, 79, 83, 88, 83, 79, 81, 85, 82, 85, 82, 84, 81, 85, 84, 82, 80, 81, 80,
              87, 79, 88, 94, 89, 87, 91, 88, 89, 98, 86, 94, 94, 101, 89, 95, 94, 90])

plt.subplot(3, 1, 1)
plt.plot(x, y, label='manual measurement')
plt.plot(x, diameter1_array[1:59], label='square')
plt.legend()
print("deviation1", sum(abs(y - diameter1_array[1:59])))
print("standard deviation1", np.std(abs(y - diameter1_array[1:59])))

plt.subplot(3, 1, 2)
plt.plot(x, y, label='manual measurement')
plt.plot(x, diameter2_array[1:59], label='inner_circle')
plt.legend()
print("deviation2", sum(abs(y - diameter2_array[1:59])))
print("standard deviation2", np.std(abs(y - diameter2_array[1:59])))


plt.subplot(3, 1, 3)
plt.plot(x, y, label='manual measurement')
plt.plot(x, diameter3_array[1:59], label='outer_circle')
plt.legend()
print("deviation3", sum(abs(y - diameter3_array[1:59])))
print("standard deviation3", np.std(abs(y - diameter3_array[1:59])))

plt.xlabel("apple_num")


plt.show()
print("diameter_array", diameter1_array)
cv2.waitKey(0)
cv2.destroyAllWindows()
