from minio import Minio
from ultralytics import YOLO
import torch
import train_config as config

client = Minio(
    endpoint="minio.smtornado.ru",
    access_key=None,
    secret_key=None,
    secure=True
)

try:
    client.fget_object(config.bucket_name, config.file_name, config.destination)
    print(f"File '{config.file_name}' downloaded successfully to '{config.destination}'.")
except Exception as err:
    print(f"Error occurred: {err}")

model = YOLO(config.model_name)

# Train the model on the yolo_dataset
results = model.train(
  data=config.destination,
  epochs=config.epochs,
  imgsz=config.image_size,
  plots=True,
  device=torch.device(torch.device('cuda')),
  conf=config.confidence
)
