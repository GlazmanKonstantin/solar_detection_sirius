from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = FastAPI()

@app.get("/image")
def get_image():
    path = r"C:\Users\user\Downloads\sun.png"
    img = Image.open(path)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf8")
    
    return {"image": "generated.png", "base64": image_b64}
