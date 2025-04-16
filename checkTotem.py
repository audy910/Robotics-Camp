import cv2
import numpy as np
import time
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from picamera2 import Picamera2

# Load the model
model = load_model("/home/robotics/Downloads/RoboCarV1.keras")

# Define labels
class_labels = ["green", "red", "yellow"]

# Initialize camera
camera = Picamera2()
camera.start()

try:
    while True:
        frame = camera.capture_array()

        # Resize and preprocess the frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        resized = cv2.resize(frame_rgb, (150, 150))

        image = img_to_array(resized) / 255.0
        image = np.expand_dims(image, axis=0)

        # Predict
        prediction = model.predict(image)
        class_index = np.argmax(prediction[0])
        label = class_labels[class_index]

        print(f"Totem Color: {label}")

        # Break on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    camera.stop()
    cv2.destroyAllWindows()

