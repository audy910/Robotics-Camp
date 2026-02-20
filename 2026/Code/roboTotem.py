import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2
from picamera2.encoders import Quality
from ultralytics import YOLO

# Load the YOLO model once
model_path="PASTE_FILE_PATH_HERE"
model = YOLO(model_path, task='detect')
labels = model.names

# Define threshold
confidence_threshold = 0.8

# #Initialize camera once
camera = Picamera2()
camera.start()

def viewTotem():
    global num_frames
    try:
        frame = camera.capture_array()
        frame = cv2.cvtColor(np.copy(frame), cv2.COLOR_BGRA2BGR)
        results = model.track(frame, verbose=False)
        detections = results[0].boxes
        confidence = 0
        if detections is not None and len(detections) > 0:
            det = detections[0]
            classidx = int(det.cls.item())
            confidence = det.conf.item()
        print(f"confidence: {confidence}")
        if confidence >=  confidence_threshold:
            return labels[classidx]
        return "no"
        
    except Exception as e:
        print("Error in viewTotem():", type(e).__name__)
        return "no"
