import serial
import time
import board
import pigpio
from adafruit_motorkit import MotorKit
import cv2
import numpy as np
import tensorflow as tf
from picamera2 import Picamera2
from picamera2.encoders import Quality
from checkTotem import viewTotem

# Setup
kit = MotorKit(i2c=board.I2C())
pi = pigpio.pi()
if not pi.connected:
    exit()

servo_gpio = 4		

# Center servo
pi.set_servo_pulsewidth(servo_gpio,800)
time.sleep(1)
pi.set_servo_pulsewidth(servo_gpio,0)

#Decide command
yolo_command = None
yolo_time = 0
prev_totem = 'none'
prev_time = 0

bluetooth_command = None
bluetooth_time = 0

# Serial setup for Bluetooth
try:
    ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
    print("rfcom0")
except serial.SerialException:
    ser = serial.Serial("/dev/rfcomm1", 9600, timeout=1)
    print("rfcom1")
ser.reset_input_buffer()

# Initial motor speeds
speed_left = 0
speed_right = 0
kit.motor1.throttle = speed_left
kit.motor2.throttle = speed_right

# Duty cycles for servo directions
SERVO_CENTER = 1000
SERVO_RIGHT = 850       
SERVO_LEFT = 1150
SERVO_STOP = 0

last = 0

def decide():
    now = time.time()
    if yolo_time > now:
        return yolo_command
    elif bluetooth_command and now - bluetooth_time < 2:
        return 'bluetooth'
    return None
   
def get_bluetooth():
    return bluetooth_command

try:
    while True:
        curr = time.time()
        if curr - last > 2:
            totem = viewTotem()
            print(totem)
            last = curr
        else:
            totem = "no"
            
        if totem != "no":
            yolo_command = totem
            if totem == 'green' and (prev_totem != 'green' or time.time() > prev_time):
                yolo_time = time.time() + 1.5
                prev_time = time.time() + 5.0
                prev_totem = 'green'
            elif totem == 'yellow' and (prev_totem != 'yellow' or time.time() > prev_time):
                yolo_time = time.time() + 2.0
                prev_totem = 'yellow'
                prev_time =time.time() + 5.0
            elif totem == 'red' and (prev_totem != 'red' or time.time() > prev_time):
                yolo_time = time.time() + 1.5
                prev_totem = 'red'
                prev_time = time.time() + 5.0
            time.sleep(0.1)                                                                                                                                                                               
        
        else:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    try:
                        values = line.split(',')
                        if len(values) != 2:
                            continue
                        throttle = values[0]
                        direction = values[1]
                        print(throttle)
                        print(direction)
                        
                        # Control speed
                        throttle_val = int(throttle)
                        if throttle_val > 500 and throttle_val < 570:
                            speed_left = speed_right = 0
                        elif throttle_val > 512:
                            val = ((throttle_val - 512) / 512)
                            speed_left = speed_right = min(0.8, val)
                        elif throttle_val < 512:
                            val = -((512 - throttle_val) / 512)
                            speed_left = speed_right = max(-0.8, val)
                            
                        #Control direction
                        if direction == "l":
                            servo_direction = SERVO_LEFT
                        elif direction == "r":
                            servo_direction = SERVO_RIGHT
                        elif direction == "i":
                            servo_direction = SERVO_CENTER
                        
                        bluetooth_command = (speed_left, speed_right, servo_direction)
                        bluetooth_time = time.time()
                    
                    except ValueError:
                        continue
                    
        command = decide()
        if command == 'red':
            print("red")
            speed_left = speed_right = 0.99
            kit.motor1.throttle = speed_left
            kit.motor2.throttle = speed_right
            pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)
            ser.reset_input_buffer()
    
        elif command == 'yellow':
            print("yellow")
            gesture_time = time.time()
            kit.motor1.throttle = 0.5
            kit.motor2.throttle = 0.75
            if yolo_time - 1.0 < gesture_time < yolo_time:
                kit.motor1.throttle = 0.75
                kit.motor2.throttle = 0.5
            pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)
            ser.reset_input_buffer()
             
        elif command == 'green':
            print("green")
            speed_left = speed_right = 0
            kit.motor1.throttle = speed_left
            kit.motor2.throttle = speed_right
            pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)
            ser.reset_input_buffer()
 
        elif command == 'bluetooth':
            speed_left, speed_right, servo_direction = get_bluetooth()
            kit.motor1.throttle = speed_left
            kit.motor2.throttle = speed_right
            pi.set_servo_pulsewidth(servo_gpio, servo_direction)
            
        else:
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0
            pi.set_servo_pulsewidth(servo_gpio, 0)
            
except Exception:
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    pi.set_servo_pulsewidth(servo_gpio, 0) 
    pi.stop()  
    
except KeyboardInterrupt:
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    pi.set_servo_pulsewidth(servo_gpio, 0) 
    pi.stop()      