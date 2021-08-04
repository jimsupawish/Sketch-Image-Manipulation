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
from skimage import io, color, filters, util, restoration
import time

use_invert = True
use_gaussian = True
mask_at_end = True
sobel_threshold = 0.005
sobel_mult = 4
sobel_offset = 0.0
bucket_size = 16
bucket_max_threshold = 255 - (bucket_size // 2 - 1)

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

def apply_bucket(val):
    if (val >= bucket_max_threshold):
        return 255
    else:
        return (val // bucket_size) * bucket_size

# Separate each RGB element into buckets
# Concepts from using toon shader
def use_bucket(image):
    # Use vectorize to apply function to each element in the array
    # https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html
    # https://stackoverflow.com/questions/42594695/how-to-apply-a-function-map-values-of-each-element-in-a-2d-numpy-array-matrix
    apply_bucket_vec = np.vectorize(apply_bucket)
    return apply_bucket_vec(image)

def pick_color_at_edge(image, sobel_image):
    color_mask = sobel_image > 0.92
    image[color_mask] = 1
    return image

def process_cartoon_effect(image, sobel_image):
    mask = sobel_image < 0.92
    image[mask] = sobel_image[mask] * 0.35
    # for i in range(0, len(image)):
    #     for j in range(0, len(image[0])):
    #         for k in range(3):
    #             if (sobel_image[i][j][k] < 0.9):
    #                 image[i][j][k] = sobel_image[i][j][k] * 0.35
    return image

def process_save(save_enabled, filename):
    # https://stackoverflow.com/questions/39870642/matplotlib-how-to-plot-a-high-resolution-graph
    if (save_enabled):
        # <filename>_generated.<ext>
        save_name = filename[:max(0, filename.rfind("."))] + "_generated" + filename[filename.rfind("."):]
        plt.savefig(fname=save_name, dpi=600)

def draw_sketch(filename, image, image_sobel, use_edge_as_color, cartoon_effect, save_enabled):
    plt.axis('off')
    plt.tight_layout()
    start_time = time.perf_counter()
    if use_edge_as_color:
        new_image = pick_color_at_edge(image, image_sobel)
        plt.imshow(new_image)
        print("Pick Color at edge takes " + str(time.perf_counter() - start_time) + " seconds.")
    elif cartoon_effect:
        new_image = process_cartoon_effect(image, image_sobel)
        plt.imshow(new_image)
        print("Cartoon effect takes " + str(time.perf_counter() - start_time) + " seconds.")
    else:
        plt.imshow(image_sobel, cmap=plt.cm.gray)
        print("Default effect takes " + str(time.perf_counter() - start_time) + " seconds.")

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
    # Use perf_counter as a stopwatch from https://realpython.com/python-timer/
    start_time = time.perf_counter()
    abs_start = start_time
    image = io.imread(filename)

    if (image.shape[2] == 4):
        image = color.rgba2rgb(image)

    print("Read image takes " + str(time.perf_counter() - start_time) + " seconds.")
    start_time = time.perf_counter()
    original_image = image.copy()
    print("Copy image takes " + str(time.perf_counter() - start_time) + " seconds.")
    start_time = time.perf_counter()
    image = restoration.denoise_bilateral(image, win_size=5, multichannel=True)
    print("Bilateral filter takes " + str(time.perf_counter() - start_time) + " seconds.")
    start_time = time.perf_counter()
    # image = use_bucket(image)
    # print("Bucketing takes " + str(time.perf_counter() - start_time) + " seconds.")
    # start_time = time.perf_counter()

    # Separate into R, G, B channels
    image_r = image[:,:,0]
    image_g = image[:,:,1]
    image_b = image[:,:,2]

    print("Set up rgb array takes " + str(time.perf_counter() - start_time) + " seconds.")
    start_time = time.perf_counter()

    # Do Sobel Filter
    image_r_sobel = apply_sobel_filter(image_r)
    image_g_sobel = apply_sobel_filter(image_g)
    image_b_sobel = apply_sobel_filter(image_b)
    image_sobel_combined = image_r_sobel + image_g_sobel + image_b_sobel

    print("All RGB sobel filters take " + str(time.perf_counter() - start_time) + " seconds.")
    start_time = time.perf_counter()
    
    if mask_at_end:
        image_sobel_combined = apply_drawing_mask(image_sobel_combined)
        print("Apply drawing mask takes " + str(time.perf_counter() - start_time) + " seconds.")
        start_time = time.perf_counter()
    if use_invert and (not dark_mode):
        image_sobel_combined = util.invert(image_sobel_combined)
        print("Invert image takes " + str(time.perf_counter() - start_time) + " seconds.")
        start_time = time.perf_counter()
    
    image_sobel_combined_rgb = color.gray2rgb(image_sobel_combined)

    if use_subplots:
        draw_original(original_image)
        print("Plot original image takes " + str(time.perf_counter() - start_time) + " seconds.")
    draw_sketch(filename, image, image_sobel_combined_rgb, use_edge_as_color, cartoon_effect, save_enabled)
    abs_end = time.perf_counter()
    print("TOTAL TIME TAKEN = " + str(abs_end - abs_start) + " seconds.")