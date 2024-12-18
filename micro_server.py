from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = FastAPI()

@app.get("/datetime")
def get_data():
    return {"datetime": "datetime"}

# Build
# pip install fastapi uvicorn
# uvicorn micro_server:app --reload
