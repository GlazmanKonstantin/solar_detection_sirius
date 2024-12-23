from PIL import Image, ImageDraw
import os
import glob
import sys

import astropy
from astropy.io import fits

from converter import FitsConverter
from math import pi, degrees, sin, cos

PATH = r'C:\Users\user\Downloads\test\aia.lev1_euv_12s.2021-01-01T000610Z.171.image_lev1.fits'

PATH_OUTPUT_SUN = r'C:\Users\user\Downloads'
PATH_FITS = r'C:\Users\user\Downloads\test'
PATH_CSV = r'C:\Users\user\Downloads\test\trash.csv'
PATH_IMG = r'C:\Users\user\Downloads\test1'
PATH_PREDICT_YOLO = r'C:\Users\user\Downloads\2021-01-04T050010Z_3.txt'

def make_seg(yolo_predict, fits_file, color = "red"):
    FitsConverter(PATH_IMG, PATH_CSV, '', PATH_FITS, verbose=False).convert()
    im = Image.open(r'C:\Users\user\Downloads\test1\aia.lev1_euv_12s.2021-01-01T000610Z.171.image_lev1_boundary.png').convert('RGB')
    len_line = im.size[0]
    widthBBox = 2
    head = fits_file[1].header
    RSUN = head["R_SUN"]
    sun_x_c = head["CRPIX1"]
    sun_y_c = head["CRPIX2"]
    with open(yolo_predict) as txt_LINE:
        LINE = txt_LINE.readline()
        
        X_center, Y_center, W, H = [float(x) for x in LINE.split()[1:]]
        x0 = X_center - W / 2
        x1 = X_center + W / 2
        
        a_st = x0 * 2 * pi - pi / 2
        a_fi = x1 * 2 * pi - pi / 2
        if a_st < 0:
            a_st += 2 * pi
        if a_fi < 0:
            a_fi += 2 * pi
        
        
        y0 = Y_center - H / 2
        y1 = Y_center + H / 2

        y_st = y0
        y_fi = y1
        
        r_st = RSUN + y_st
        r_fi = RSUN + y_fi
     
    im_SUN= Image.fromarray(fits_file[1].data).convert('RGB')
    draw = ImageDraw.Draw(im_SUN)
    
    #print(im_SUN.size)
    
    draw.arc((sun_x_c - r_st, sun_y_c - r_st, sun_x_c + r_st, sun_y_c + r_st), degrees(a_st), degrees(a_fi), color, widthBBox)
    draw.arc((sun_x_c - r_fi, sun_y_c - r_fi, sun_x_c + r_fi, sun_y_c + r_fi), degrees(a_st), degrees(a_fi), color, widthBBox)
    
    a_st += pi / 2
    a_fi += pi / 2
    draw.line([(sun_x_c + r_st * sin(a_st),
                sun_y_c - r_st * cos(a_st)),
                (sun_x_c + r_fi * sin(a_st),
                sun_y_c - r_fi * cos(a_st)) ], color, widthBBox)
    draw.line([(sun_x_c + r_st * sin(a_fi),
                sun_y_c - r_st * cos(a_fi)),
                (sun_x_c + r_fi * sin(a_fi),
                sun_y_c - r_fi * cos(a_fi))], color, widthBBox)
    
    print(im_SUN)
    im_SUN.show()
    

if __name__ == "__main__":
    fits_file=fits.open(PATH)
    make_seg(PATH_PREDICT_YOLO, fits_file)
