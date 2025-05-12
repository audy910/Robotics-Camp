import serial
from picarx import Picarx
import time
from picamera2 import Picamera2

ser = serial.Serial("/dev/rfcomm0", 9600, timeout = 1)

ser.reset_input_buffer()

# init picarx
px = Picarx()

camera = Picamera2()


#count = 1

speed = 10
px.set_dir_servo_angle(7)
while True:
    line = ser.read().decode("utf-8")
    print(line)
    if('1' in line):
        speed = 100
        px.set_dir_servo_angle(7)
        px.forward(speed)
        print(line)
    elif('2' in line):
        px.set_dir_servo_angle(30)
        print(line)
    elif('3' in line):
        px.set_dir_servo_angle(-22)
        print(line)
    elif('4' in line):
        speed = 0
        px.forward(speed)
        print(line)
#    if(speed > 0):
#        camera.start()
#        camera.capture_file('/home/robotics/Desktop/dataset/rpicam_image_red'+str(count)+'.jpg')
#         count+=1
#         camera.stop()
