#here i finetune the tesserac model:
#import tesserac
import torch
from pathlib import Path
#import tesstrain
currentdir = Path.cwd()
oneup = currentdir.parents
pathoftrainingdata = oneup / " OCR_training_data"

print(pathoftrainingdata)
