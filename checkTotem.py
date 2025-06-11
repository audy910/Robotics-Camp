import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2

# Load the TFLite model once
interpreter = tf.lite.Interpreter(model_path="/home/robotics/Downloads/model_quant.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define class labels and threshold
class_labels = ["green", "red", "yellow"]
confidence_threshold = 0.70

# Initialize camera once
camera = Picamera2()
camera.start()

def viewTotem():
    try:
        frame = camera.capture_array()

        # Convert and resize
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        resized = cv2.resize(frame_rgb, (150, 150), interpolation=cv2.INTER_AREA)

        # Normalize and reshape
        image = np.expand_dims(resized.astype(np.float32) / 255.0, axis=0)

        # Set tensor and run inference
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        class_index = int(np.argmax(output_data[0]))
        confidence = float(output_data[0][class_index])

        if confidence >= confidence_threshold:
            return class_labels[class_index]
        else:
            return "no"
    except Exception as e:
        print("Error in viewTotem():", e)
        return "no"
while True:
    print(viewTotem())