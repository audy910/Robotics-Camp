import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array

# Load the model
model = load_model("totem_model.keras")

# Define labels (order must match OneHotEncoder during training!)
class_labels = ["Green", "Red", "Yellow"]

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize and preprocess the frame
    resized = cv2.resize(frame, (150, 150))
    image = img_to_array(resized) / 255.0
    image = np.expand_dims(image, axis=0)

    # Predict
    prediction = model.predict(image)
    class_index = np.argmax(prediction[0])
    label = class_labels[class_index]

    # Output to terminal (no drawing on the frame)
    print(f"Totem Color: {label}")

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
