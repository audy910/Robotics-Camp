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

        # Take out Alpha channel from the frame captured, only RGB necessary for training, so only 3 channels
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)                
        
        # Resize to 150 by 150 to match model input size        
        resized = cv2.resize(frame_rgb, (150, 150), interpolation=cv2.INTER_AREA)   

        # Normalize pixel values [0, 1] and adds dimension of size 1 to front of the image array making it [1, 150, 150, 3]
        image = np.expand_dims(resized.astype(np.float32) / 255.0, axis=0) 

        # Use trained model to return output_daya array with predicted values for each color 
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Find largest value in the array and that will be the predicted color, and grab its confidence
        class_index = int(np.argmax(output_data[0]))
        confidence = float(output_data[0][class_index])

        # If the confidence is greater than the confidence_threshold then prints the predicted color
        label = class_labels[class_index]
        if confidence >= confidence_threshold:
            return class_labels[class_index]
        else:
            return "no"
        
    except Exception as e:
        print("Error in viewTotem():", e)
        return "no"
    
while True:
    print(viewTotem())