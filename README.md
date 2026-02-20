# Robotics-Camp

## 2026 Pipeline
The figure below represents our intended pipeline from the Arduino controller to the Raspberry Pi robotic car.

```
(1) trainYOLO.ipynb --> (2) controller.ino --> (3) roboFull.py & roboTotem.py
```

#######################################################################################
### Personal Computer

**(1)** We will download the dataset via Roboflow (link provided below). Go to the most recent version (Version 7) and click on **Download Dataset**. A popup will appear. Ensure that the image and annotation format is YOLOv11, and under Download Options select **Show Download Code**, then continue. Copy the provided snippet.

Roboflow: https://app.roboflow.com/lab-t8ma7/robotics-camp-cyjqi/7

**(2)** Log into Google Colab and upload the `trainYOLO.ipynb` file. Copy and paste the snippet from Roboflow into the fourth cell where it says "PASTE ROBOFLOW SNIPPET HERE".

**(3)** After running all of the cells, click on the Files section in the sidebar and download the `best_float_32.tflite` file. The path to retrieve the file is below.

```bash
├── Files
│   ├── runs
│   │   ├── detect
│   │   │   ├── train
│   │   │   │   ├── weights
│   │   │   │   │   ├── best_saved_model
│   │   │   │   │   │   ├── best_float_32.tflite
```

**(4)** Upload the file to your Google Drive.

### Arduino Bluetooth Controller
**(5)** Follow the schematic design under Documentation labeled `BluetoothSchematics.jpg`.

**(6)** Plug the standard USB Type-B cable into the Arduino and your laptop. The Bluetooth module will blink a red light, indicating that it is connected correctly.

**(7)** Upload the `controller.ino` file to your laptop and open it in the Arduino IDE.

**(8)** Click on Verify, then click on Upload to put the code onto the Arduino. It is working correctly if a red light is blinking on the Bluetooth module, indicating that it was wired correctly, and if the output of the Serial Monitor is continuously printing something similar to the example below:

```bash
-----
Joystick Left: X = 493, Y = 490
Joystick Right: X = 514, Y = 516
490, i
-----
```

**(9)** Unplug the standard USB Type-B cable from the Arduino. Connect a battery to the DC adapter. Ensure that the red light is blinking on the Bluetooth module while the battery is connected.

### Raspberry Pi
**(10)** Click on the Bluetooth icon in the upper right corner and connect to DSD TECH HC-05. If connected correctly, the Bluetooth icon should turn green.

**(10)** Upload the `roboFull.py` and `roboTotem.py` files.

**(11)** Log into Google Drive.

**(12)** Download the `best_float_32.tflite` file from your Google Drive. Afterwards, it should now be in the Downloads folder on the Raspberry Pi. Copy the path of the file.

**(13)** In the `roboTotem.py` file, on line 9, paste the path of the file where it says "PASTE_FILE_PATH_HERE".

**(14)** Run `roboFull.py`.

## Additional Notes
Under Additional Resources, there are scripts for the Raspberry Pi to test functionality. `yoloTest.py` tests the computer vision aspect without the motor controls. `motorTest.py` tests the motor controls without the computer vision aspect.