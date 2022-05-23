import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import cv2
import random
from tqdm import tqdm
import os
import json
import datetime

from lib.denoise import denoise

lower_green = np.array([[55, 20, 20]])
upper_green = np.array([[80, 255, 255]])
blur_kernel = (5, 5)
dilate_kernel = (5, 5)
denoise_temp_size = 50
denoise_window_size = 50
denoise_strength = 20

def get_on_change(window_name, image):
    def on_change(key):
        def change(value):
            global lower_green, upper_green, blur_kernel, dilate_kernel, denoise_temp_size, denoise_window_size, denoise_strength
            if key == 'lhh':
                lower_green[0][0] = value
            elif key == 'lhs':
                lower_green[0][1] = value
            elif key == 'lhb':
                lower_green[0][2] = value
            elif key == 'uhh':
                upper_green[0][0] = value
            elif key == 'uhs':
                upper_green[0][1] = value
            elif key == 'uhb':
                upper_green[0][2] = value
            elif key == 'blur':
                blur_kernel = (value, value)
            elif key == 'dilate':
                dilate_kernel = (value, value)
            elif key == 'dts':
                denoise_temp_size = value
            elif key == 'dws':
                denoise_window_size = value
            elif key == 'ds':
                denoise_strength = value
            redraw(window_name, image)
        return change
    return on_change


def redraw(window_name, image):
    new_image = image.copy()

    denoise_mask = denoise(
        new_image,
        lower_green=lower_green,
        upper_green=upper_green,
        denoise_temp_size=denoise_temp_size,
        denoise_window_size=denoise_window_size,
        denoise_strength=denoise_strength,
        blur_kernel=blur_kernel,
        dilate_kernel=dilate_kernel
    )

    cv2.imshow(window_name, denoise_mask)


def plot_image(image_file):
    image = cv2.imread(image_file)
    height, width, _ = image.shape

    window_name = 'window'

    redraw(window_name, image)

    on_change = get_on_change(window_name, image)

    cv2.createTrackbar('lower hsv hue', window_name, 0, 255, on_change('lhh'))
    cv2.createTrackbar('lower hsv sat', window_name, 0, 255, on_change('lhs'))
    cv2.createTrackbar('lower hsv brt', window_name, 0, 255, on_change('lhb'))
    cv2.createTrackbar('upper hsv hue', window_name, 0, 255, on_change('uhh'))
    cv2.createTrackbar('upper hsv sat', window_name, 0, 255, on_change('uhs'))
    cv2.createTrackbar('upper hsv brt', window_name, 0, 255, on_change('uhb'))
    cv2.createTrackbar('blur', window_name, 0, 100, on_change('blur'))
    cv2.createTrackbar('dilate', window_name, 0, 100, on_change('dilate'))
    cv2.createTrackbar('denoise temp', window_name, 0, 100, on_change('dts'))
    cv2.createTrackbar('denoise window', window_name, 0, 100, on_change('dtw'))
    cv2.createTrackbar('denoise stre', window_name, 0, 100, on_change('ds'))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


plot_image('./many_plants_2.jpg')