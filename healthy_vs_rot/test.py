import os
import keras
import numpy as np
import tensorflow as tf
import cv2
from keras.applications import VGG16

conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(150, 150, 3))

mo1 = keras.models.load_model('/home/jon/Graduation_project/healthy_vs_rot/healthy_vs_rot_1.h5')

mo1.summary()

healthy = '/home/jon/Graduation_project/healthy_vs_rot/test/healthy'
rot = '/home/jon/Graduation_project/healthy_vs_rot/test/rot'
healthy_img = os.listdir(healthy)
rot_img = os.listdir(rot)

for img1 in healthy_img:

    img = cv2.imread('/home/jon/Graduation_project/healthy_vs_rot/test/healthy/' + img1)
    res = cv2.resize(img, (150, 150))
    res = res/255
    res = res[np.newaxis, :]
    res = conv_base.predict(res)
    res = np.reshape(res, (1, 4 * 4 * 512))
    ans = mo1.predict(res)
    print(ans, end=' ')
    print(img1)

print("------------------------------------------------")

for img2 in rot_img:

    img = cv2.imread('/home/jon/Graduation_project/healthy_vs_rot/test/rot/' + img2)
    res = cv2.resize(img, (150, 150))
    res = res/255
    res = res[np.newaxis, :]
    res = conv_base.predict(res)
    res = np.reshape(res, (1, 4 * 4 * 512))
    ans = mo1.predict(res)
    print(ans, end=' ')
    print(img2)

