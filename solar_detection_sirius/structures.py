import requests
from PIL import Image
import streamlit as st
import datetime
import os
import glob
import time
import av
import shutil
from os import listdir
# from pygments.styles.dracula import yellow
from streamlit import markdown, divider, selectbox
from seg import make_seg
import astropy
from astropy.io import fits
from constants import PATH_TMP, PATH_FITS, PATH_LABELS, PATH_IMAGES
from constants import BASE_URL

def pngs_to_h264_mp4(input_folder, output_file, frame_rate=30):
    """
    Converts a sequence of PNG images to an H.264 MP4 file using PyAV.
    
    Parameters:
    - input_folder: Path to the folder containing PNG images.
    - output_file: Path to the output MP4 file.
    - frame_rate: Frame rate for the video.
    """
    # Ensure the input folder exists
    if not os.path.isdir(input_folder):
        raise ValueError(f"The folder '{input_folder}' does not exist.")
    
    # Get sorted list of PNG files in the folder
    png_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".png")])
    if not png_files:
        raise ValueError(f"No PNG files found in the folder '{input_folder}'.")

    # Open the output file for video writing
    container = av.open(output_file, 'w')
    stream = container.add_stream("h264", rate=frame_rate)
    stream.width = 768  # Adjust width (should match your image dimensions)
    stream.height = 384  # Adjust height (should match your image dimensions)
    stream.pix_fmt = "yuv420p"

    for png_file in png_files:
        img_path = os.path.join(input_folder, png_file)
        with Image.open(img_path) as img:
            frame = av.VideoFrame.from_image(img)
            for packet in stream.encode(frame):
                container.mux(packet)
    
    # Flush remaining packets and close the file
    for packet in stream.encode(None):
        container.mux(packet)
    container.close()
    print(f"Video saved to {output_file}")


def get_image(d):
    os.chdir(PATH_IMAGES)
    ls = list(glob.glob(f"{d}*.png"))
    gl_fl=False
    img = []
    name = ''
    for i in range(len(ls)):
        file=ls[i]
        shutil.copy(os.path.join(PATH_IMAGES, file), PATH_TMP)
        os.chdir(PATH_FITS)
        ls1 = list(glob.glob('*'+file[:-7]+'*.fits'))
        if len(ls1)==0:
            continue
        fits_file = ls1[0]
        os.chdir(PATH_LABELS)
        ls1= list(glob.glob(file[:-4]+'.txt'))
        if len(ls1)==0:
            continue
        label = ls1[0]
        path_fits=os.path.join(PATH_FITS, fits_file)
        if i==0:
            img=Image.fromarray(fits.open(path_fits)[1].data).convert('RGB')
        [img, fl] = make_seg(os.path.join(PATH_LABELS, label), path_fits, img)
        #st.image(img)
        name = file[:-4]+'.png'
        if fl:
            gl_fl=True
    #img.save(os.path.join(tmp_folder, name))
    if type(img)!='list':
        st.image(img)
    return gl_fl


def get_video(d):
    # TODO: write the fucntion with get_image
    output_file = 'output_video.mp4'
    fps = 2  # Frames per second
    pngs_to_h264_mp4(PATH_TMP, output_file, fps)
    video_file = open(output_file, "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)
    video_file.close()
    os.remove(output_file)
    os.chdir(PATH_TMP)
    ls = list(glob.glob('*'))
    for el in ls:
        os.remove(el)

def get_time(d):
    os.chdir(PATH_IMAGES)
    ls = list(glob.glob(f"{d}*.png"))
    if d is None:
        return
    if len(ls) == 0:
        st.write("No images on this date")
    else:
        time_ = ['None']
        for file in ls:
            tm = file[file.find('T') + 1: file.rfind('Z')]
            tm = tm[:2] + '-' + tm[2:4] + '-' + tm[4:]
            time_.append(tm)
        s = set()
        ans= []
        for el in time_:
            if el not in s:
                s.add(el)
                ans.append(el)
        return [ans, ls]

def get_name_time(s, d):
    return str(d)+'T'+s[:2]+s[3:5]+s[6:8]+'Z'

def ask_datetime():
    response = requests.get(f"http://127.0.0.1:8000/datetime")
    if response.status_code == 200:
        d = st.date_input("Your date", value=None, min_value=datetime.date(1950, 1, 1),
                          max_value=datetime.datetime.now(),
                          help="specify the date on which you want to see what the sun will be like",
                          format="DD/MM/YYYY")              
        time_ = get_time(d)
        if time_ is not None:
            t = st.selectbox("Your time", time_[0])
            st.write('Please wait several minutes...')
            get_image(get_name_time(t, d))


st.header("Structures in the Sun", divider="orange")
ask_datetime()
