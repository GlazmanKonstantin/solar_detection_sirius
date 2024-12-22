import requests
from PIL import Image
import streamlit as st
import datetime
import os
import glob
import time

# from pygments.styles.dracula import yellow
from streamlit import markdown, divider, selectbox

BASE_URL = "http://127.0.0.1:8000"
PATH = r"C:\Users\Katia\Downloads\dataset_yolo\dataset_yolo\train\images"


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
        except:
            st.write("ERROR in date")



st.header("Structures in the Sun", divider="orange")
ask_datetime()