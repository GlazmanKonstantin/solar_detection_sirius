from PIL import Image, ImageDraw
import os
import glob
import sys

import astropy
from astropy.io import fits

from os import listdir
from converter import FitsConverter
import shutil
from fnmatch import fnmatch
from math import pi, degrees, sin, cos
from constants import DIGITIZATION_SIZE, IMGSZ, Y_IMGSZ, SEGMENT_COUNT
import numpy as np

PATH_OUTPUT_SUN = r'C:\Users\user\Downloads'
PATH_FOLDER = r'C:\Users\user\Downloads\tmp'

def get_len(fits_file, path_fits):
    shutil.copy(path_fits, PATH_FOLDER)
    FitsConverter(PATH_FOLDER, PATH_FOLDER + r'\trash.csv', '', PATH_FOLDER, verbose=False).convert()
    len_line = 0
    os.chdir(PATH_FOLDER)
    ls = list(glob.glob("*.png"))
    for f in ls:
        im = Image.open(f)
        len_line = im.size[0]
    return len_line

def get_start(s):
    seg_start = np.arange(SEGMENT_COUNT) * (
        DIGITIZATION_SIZE // SEGMENT_COUNT
    )
    s = s.split('_')[1]
    s = s.split('.txt')[0]
    return seg_start[int(s)]

def make_seg(path_yolo_predict, path_fits, im_SUN, color = "red"):
    yolo_predict = open(path_yolo_predict)
    fits_file= fits.open(path_fits)
    len_line = get_len(fits_file, path_fits)
    x__1 = get_start(yolo_predict.name)
    x__2 = x__1 + IMGSZ
    widthBBox = 10
    head = fits_file[1].header
    RSUN = head["R_SUN"]
    dR = Y_IMGSZ
    sun_x_c = head["CRPIX1"]
    sun_y_c = head["CRPIX2"]

    X1 = x__1 / len_line
    X2 = x__2 / len_line

    x_len = X2 - X1
    if X1 > X2:
        x_len = 1 - X2 + X1
    
    X_c = 0.0
    Y_c = 0.0
    W = 0.0
    H = 0.0
    with open(path_yolo_predict) as txt_LINE:
        LINE = txt_LINE.readlines()
        inp = [[float(x) for x in line.split()] for line in LINE]
    draw = ImageDraw.Draw(im_SUN)
    for (X_c, Y_c, W, H) in inp:
        x_rel1 = X_c - W / 2
        x_rel2 = X_c + W / 2

        isThree = False
        if x_rel1 < 0:
            x_rel1 += 1
            isThree = True
        if x_rel2 > 1:
            x_rel2 -= 1
            isThree = True
            
        x_1 = X1 + x_rel1 * x_len
        x_2 = X1 + x_rel2 * x_len

        a__st = x_1 * 2 * pi
        a__fi = x_2 * 2 * pi
        
        x_cir_1 = 1 - x_1
        x_cir_2 = 1 - x_2
            
        a_st = x_cir_1 * 2 * pi
        a_fi = x_cir_2 * 2 * pi

        y_rel1 = Y_c - H / 2
        y_rel2 = Y_c + H / 2

        y1 = (1 - y_rel1) * dR
        y2 = (1 - y_rel2) * dR

        r_st = RSUN + y1
        r_fi = RSUN + y2
        
        #print(im_SUN.size)
        if isThree:
            draw.arc((sun_x_c - r_st,
                    sun_y_c - r_st,
                    sun_x_c + r_st,
                    sun_y_c + r_st), degrees(a__st), 360, color, widthBBox)
            draw.arc((sun_x_c - r_st,
                    sun_y_c - r_st,
                    sun_x_c + r_st,
                    sun_y_c + r_st), 0, degrees(a__fi), color, widthBBox)
        else:
            draw.arc((sun_x_c - r_st,
                    sun_y_c - r_st,
                    sun_x_c + r_st,
                    sun_y_c + r_st), degrees(a__st), degrees(a__fi), color, widthBBox)
        
        if isThree:
            draw.arc((sun_x_c - r_fi,
                    sun_y_c - r_fi,
                    sun_x_c + r_fi,
                    sun_y_c + r_fi), degrees(a__st), 360, color, widthBBox)
            draw.arc((sun_x_c - r_fi,
                    sun_y_c - r_fi,
                    sun_x_c + r_fi,
                    sun_y_c + r_fi), 0, degrees(a__fi), color, widthBBox)
        else:
            draw.arc((sun_x_c - r_fi,
                    sun_y_c - r_fi,
                    sun_x_c + r_fi,
                    sun_y_c + r_fi), degrees(a__st), degrees(a__fi), color, widthBBox)
        
        
        draw.line([(sun_x_c + r_st * cos(a_st),
                    sun_y_c - r_st * sin(a_st)),
                (sun_x_c + r_fi * cos(a_st),
                    sun_y_c - r_fi * sin(a_st)) ], color, widthBBox)
        draw.line([(sun_x_c + r_st * cos(a_fi),
                    sun_y_c - r_st * sin(a_fi)),
                (sun_x_c + r_fi * cos(a_fi),
                    sun_y_c - r_fi * sin(a_fi))], color, widthBBox)
    # print(im_SUN)
    # im_SUN.show()
    return [im_SUN, len(inp)>0]

# make_seg(r'C:\Users\user\Downloads\labels\2021-01-01T000610Z_6.txt', r'C:\Users\user\Downloads\fits\aia.lev1_euv_12s.2021-01-01T000610Z.171.image_lev1.fits')
