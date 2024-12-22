import requests
from PIL import Image
import streamlit as st
import datetime
import os
import glob
import time
import av

# from pygments.styles.dracula import yellow
from streamlit import markdown, divider, selectbox

BASE_URL = "http://127.0.0.1:8000"
PATH = r"C:\Users\Katia\Downloads\dataset_yolo\dataset_yolo\train\images"
PATH_IMAGES_OF_VIDEO = r"C:\Users\user\Downloads\Telegram Desktop\images"

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

def get_video():
    input_folder = PATH_IMAGES_OF_VIDEO 
    output_file = 'output_video.mp4'
    fps = 2  # Frames per second
    pngs_to_h264_mp4(input_folder, output_file, fps)
    video_file = open(output_file, "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)
    video_file.close()
    os.remove(output_file)

def get_time(d):
    os.chdir(PATH)
    ls = list(glob.glob(f"{d}*.png"))
    if d is None:
        return
    if len(ls) == 0:
        st.write("No images on this date")
    else:
        time_ = ['None', 'All']
        for file in ls:
            tm = file[file.find('T') + 1: file.rfind('Z')]
            tm = tm[:2] + '-' + tm[2:4] + '-' + tm[4:]
            time_.append(tm)
        return time_


def get_image(d, t):
    os.chdir(PATH)
    t = t.replace('-', '')
    ls = list(glob.glob(f"{d}*{t}*.png"))
    if t == 'All':
        ls = list(glob.glob(f"{d}*.png"))
    if t == 'None':
        return
    if d is None:
        return
    if len(ls) == 0:
        st.write("No images on this date")
    else:
        for file in ls:
            img = Image.open(file)
            st.image(img)


def ask_datetime():
    response = requests.get(f"http://127.0.0.1:8000/datetime")
    if response.status_code == 200:
        d = st.date_input("Your date", value=None, min_value=datetime.date(1950, 1, 1),
                          max_value=datetime.datetime.now(),
                          help="specify the date on which you want to see what the sun will be like",
                          format="DD/MM/YYYY")
        try:
            time_ = get_time(d)
            if time_ is not None:
                t = st.selectbox("Your time", time_)
                get_image(d, t)
            get_video()
        except:
            st.write("ERROR in date")



st.header("Structures in the Sun", divider="orange")
ask_datetime()
