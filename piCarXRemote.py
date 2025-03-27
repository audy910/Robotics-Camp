import serial
from picarx import Picarx
import time
from picamera2 import Picamera2

ser = serial.Serial("/dev/rfcomm0", 9600, timeout = 1)
ser.reset_input_buffer()

# init picarx
px = Picarx()

camera = Picamera2()


count = 267
speed = 0
px.set_dir_servo_angle(7)
while True:
    line = ser.readline().decode("utf-8").rstrip()
    print(line)
    if("speed" in line):
        speed = 100
        px.set_dir_servo_angle(7)
        px.forward(speed)
        print(line)
    if("right" in line):
        px.set_dir_servo_angle(15)
        print(line)
    if("left" in line):
        px.set_dir_servo_angle(-8)
        print(line)
    if("slow" in line):
        speed = 0
        px.forward(speed)
        print(line)
    if(speed > 0):
        camera.start()
        camera.capture_file('/home/robotics/Desktop/dataset/rpicam_image'+str(count)+'.jpg')
        count+=1
        camera.stop()
        time.sleep(.1)
