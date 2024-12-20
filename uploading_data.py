import minio
from constants import DOWNLOAD_LIMIT
import os
from converter import FitsConverter, YOLOConverter
from ultralytics import YOLO


def clear(directory):
    """Deletes all files in directory"""
    for __filename in os.listdir(directory):
      if not os.path.isdir(os.path.join(directory, __filename)):
        os.remove(os.path.join(directory, __filename))


client = minio.Minio(
    endpoint="minio.smtornado.ru",
    access_key=None,
    secret_key=None,
    secure=True
)

# Connecting with minio.smtornado.ru/fits and download fixed number of files we haven't yet
downloaded = 0
fits_bucket = "fits"
destination = "images/converter_input"
for element in client.list_objects(bucket_name="fits", recursive=True):    # iterating through all files at server
    if downloaded >= DOWNLOAD_LIMIT:    # we don't want to save too many files in one run, DOWNLOAD_LIMIT is declared in constants.py
        break
    if element.is_dir:
        continue
    filename = element.object_name[41:]
    if element.object_name.endswith(".fits") and filename not in os.listdir(destination):    # if file is .fits and we haven't already downloaded this file
        try:
            client.fget_object("fits", element.object_name, os.path.join(destination, filename))
            print(f"File '{element.object_name}' downloaded successfully to '{destination}'.")
            downloaded += 1
        except Exception as err:
            print(f"Error occurred: {err}")

converter_inp_dir = "images/converter_input"
model_inp_dir = "images/model_input"
tmp_dir = "images/tmp"

# Converting downloaded data from .fits to horizontal .png images of Sun
FitsConverter(converter_inp_dir, tmp_dir).convert()
YOLOConverter(tmp_dir, model_inp_dir).convert()
clear(tmp_dir)

# Run the model with new data and save predictions to "/images/model_output"
model = YOLO("runs/detect/train/weights/best.pt")
model_out_directory = "images/model_output/"
for filename in os.listdir(model_inp_dir):
    if filename.endswith(".png"):
        result = model(os.path.join(model_inp_dir, filename))
        for r in result:
            r.save(os.path.join(model_out_directory, filename))

clear(model_inp_dir)
