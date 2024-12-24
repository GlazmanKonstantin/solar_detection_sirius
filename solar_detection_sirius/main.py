import os
from os import listdir
from converter import FitsConverter, YOLOConverter
from ultralytics import YOLO
from make_batch import make_intervals
import shutil
from constants import PATH_FITS, PATH_LABELS, PATH_IMAGES, PATH_SAUSAGES, BEST_WEIGHTS, PATH_PREDICT

os.chdir(PATH_FITS)

fc = FitsConverter(PATH_SAUSAGES, os.path.join(PATH_SAUSAGES, 'trash.csv'), '', PATH_FITS)
fc.convert()

os.chdir(PATH_SAUSAGES)
os.remove(os.path.join(PATH_SAUSAGES, 'trash.csv'))

uc = YOLOConverter(PATH_IMAGES, os.path.join(PATH_IMAGES, 'trash.csv'), '', PATH_SAUSAGES)
uc.convert()

#os.chdir(r'C:\Users\user\Downloads\images')
#os.remove(r'C:\Users\user\Downloads\images\trash.csv')

model = YOLO(BEST_WEIGHTS)

batches = make_intervals(PATH_IMAGES)

for batch in batches:
    for name in batch:
        shutil.copy(os.path.join(PATH_IMAGES, name), PATH_PREDICT)
    results = model.predict(PATH_PREDICT, batch=10)
    os.chdir(PATH_PREDICT)
    for i in listdir(PATH_PREDICT):
        os.remove(i)
    for i in range(len(results)):
        name = batch[i][:-4]+'.txt'
        with open(os.path.join(PATH_LABELS, name), "w") as file:
            for el in results[i].boxes.xywhn:
                file.write(' '.join([str(float(j)) for j in el]))
                file.write('\n')
