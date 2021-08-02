# -*- coding: utf-8 -*-
"""
@author: jimsupawish
"""

"""
Some code applied from scikit-image docs, other python documentations, and StackOverflow
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import io
from skimage import color
from skimage import filters
from skimage import feature
from skimage import exposure
from skimage import transform
from skimage import util
from skimage import restoration

use_invert = True
use_gaussian = True
mask_at_end = True
sobel_threshold = 0.005
sobel_mult = 4
sobel_offset = 0.0

def apply_drawing_mask(a):
    m = a <= sobel_threshold
    a[m] = 0
    m2 = a > sobel_threshold
    a[m2] = (a[m2] - sobel_threshold) * sobel_mult + sobel_offset
    m3 = a > 1
    a[m3] = 1
    return a

def apply_sobel_filter(array):
    if (use_gaussian):
        array = filters.gaussian(array)
    sobel_image = filters.sobel(array)
    if (not mask_at_end):
        sobel_image = apply_drawing_mask(sobel_image)
    return sobel_image

def fit_horizontal(array):
    # fit_horizontal means the image are better displayed as two rows
    # Assumes an aspect ratio of the plot view as 3:2
    return 3 * len(array) <= 1 * len(array[0])

def pick_color_at_edge(image, sobel_image):
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            if (sobel_image[i][j] > 0.92):
                for k in range(3):
                    image[i][j][k] = 1
    return image

def process_cartoon_effect(image, sobel_image):
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            if (sobel_image[i][j] < 0.9):
                for k in range(3):
                    image[i][j][k] = sobel_image[i][j] * 0.35
    return image

def process_save(save_enabled, filename):
    # https://stackoverflow.com/questions/39870642/matplotlib-how-to-plot-a-high-resolution-graph
    if (save_enabled):
        # <filename>_generated.<ext>
        save_name = filename[:max(0, filename.rfind("."))] + "_generated" + filename[filename.rfind("."):]
        plt.savefig(fname=save_name, dpi=600)

def draw_sketch(filename, image, image_sobel_combined, use_edge_as_color, cartoon_effect, save_enabled):
    plt.axis('off')
    plt.tight_layout()
    if use_edge_as_color:
        new_image = pick_color_at_edge(image, image_sobel_combined)
        plt.imshow(new_image)
    elif cartoon_effect:
        new_image = process_cartoon_effect(image, image_sobel_combined)
        plt.imshow(new_image)
    else:
        plt.imshow(image_sobel_combined, cmap=plt.cm.gray)

    process_save(save_enabled, filename)
    plt.show()

def draw_original(image):
    if fit_horizontal(image):
        fig = plt.figure()
        fig.add_subplot(2, 1, 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(image, cmap=plt.cm.gray)
        fig.add_subplot(2, 1, 2)
    else:
        fig = plt.figure()
        fig.add_subplot(1, 2, 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(image, cmap=plt.cm.gray)
        fig.add_subplot(1, 2, 2)

def process_image(filename, use_subplots, use_edge_as_color, dark_mode, cartoon_effect, save_enabled):
    image = io.imread(filename)
    original_image = image.copy()
    image = restoration.denoise_bilateral(image, win_size=11, multichannel=True)

    # Separate into R, G, B channels
    image_r = image[:,:,0]
    image_g = image[:,:,1]
    image_b = image[:,:,2]

    # Do Sobel Filter
    image_r_sobel = apply_sobel_filter(image_r)
    image_g_sobel = apply_sobel_filter(image_g)
    image_b_sobel = apply_sobel_filter(image_b)
    image_sobel_combined = image_r_sobel + image_g_sobel + image_b_sobel
    
    if mask_at_end:
        image_sobel_combined = apply_drawing_mask(image_sobel_combined)
    if use_invert and (not dark_mode):
        image_sobel_combined = util.invert(image_sobel_combined)
    
    if use_subplots:
        draw_original(original_image)
    draw_sketch(filename, image, image_sobel_combined, use_edge_as_color, cartoon_effect, save_enabled)
