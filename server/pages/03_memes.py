import streamlit as st
import requests
from PIL import Image
import datetime
import os
import glob

from streamlit_player import st_player

BASE_URL = "http://127.0.0.1:8000"
PATH = r"C:\Users\Katia\Downloads"


st.markdown("# Memes")
os.chdir(PATH)
st.image("https://avatars.mds.yandex.net/i?id=a615f9190eacb78e5780767deeb936fe_l-10698872-images-thumbs&n=13")
st.image("https://i.pinimg.com/originals/4c/d3/f1/4cd3f1b8683108f649f79c941188d90f.jpg")
st.image("https://sun9-80.userapi.com/impg/V_SIrtsCmRuQRihdBQWVmAy3m41XM5zYTjyBRw/XYW4xKb3v-Y.jpg?size=750x728&quality=96&sign=0f889c6410d349e14ce7c8b3726fa788&c_uniq_tag=IeSeyujG3qK20_6UbSnz39w2NV_CFSEWgnXKbBG8a7o&type=album")
st.image("https://i.pinimg.com/736x/a0/0b/44/a00b44a9d3c5e514b96d2802536b077b.jpg")
st.image("https://avatars.mds.yandex.net/get-znatoki/1548967/AgACAgIAAxkDAAEFtAABYshRq2Jz8KdcMtIVTCW2ZbctzuAAAhqMRvC0FKyLhxkso5pREBAAMCAAN4AAMpBA/orig")
st.image("https://i.pinimg.com/originals/16/91/73/169173c95e77b1f444b9ce84323460b7.jpg")
st.image("https://img0.reactor.cc/pics/post/Комиксы-солнце-КИНА-БУДЕТ-5706398.jpeg")
# ls = list(glob.glob(f"meme*"))
# for file in ls:
#     img = Image.open(file)
#     st.image(img)
#
