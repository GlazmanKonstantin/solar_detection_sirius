from PIL import Image, ImageDraw
import os
import glob
import sys

import astropy
from astropy.io import fits

from math import pi, degrees, sin, cos

def make_seg(color = "e", PATH_LINE_TXT, PATH_SUN, dR, RSUN, sun_x_c, sun_y_c):
    widthBBox = 1
    
    with open(PATH_LINE_TXT) as txt_LINE:
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
        y_st = y0 * dR
        y_fi = y1 * dR
        
        r_st = RSUN + y_st
        r_fi = RSUN + y_fi
    
    
    with Image.open(PATH_SUN) as im_SUN:
        draw = ImageDraw.Draw(im_SUN)
        
        print(im_SUN.size)
        
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
        
        
        im_SUN.save(PATH_SUN)
        
def seg_on_SUN(color, fits_file):
    # Get fits and make .png of SUN with BBox
    # TODO Get all info from fits and call make_set() function
    

if __name__ == "__main__":
    color = input()
    make_seg(color)
