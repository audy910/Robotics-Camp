import serial
import time
import board
import pigpio
from checkTotem import viewTotem
from adafruit_motorkit import MotorKit

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

# Serial setup for Bluetooth
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1)
ser.reset_input_buffer()

# Initial motor speeds
speed_left = 0
speed_right = 0
kit.motor1.throttle = speed_left
kit.motor2.throttle = speed_right

# Duty cycles for servo directions
SERVO_CENTER = 800
SERVO_RIGHT = 1100       
SERVO_LEFT = 600
SERVO_STOP = 0



try:
    while True:
        line = ser.read().decode("utf-8").strip()
        print(line)
        if line == "0":
            speed_left=speed_right = 0
        elif line == "1":
            speed_left = speed_right = -0.75
            pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)

        elif line == "2":
            speed_left = -.75
            speed_right =- 0.5
            pi.set_servo_pulsewidth(servo_gpio,SERVO_RIGHT)


        elif line == "3":
            speed_left = -0.5
            speed_right =- 0.75
            pi.set_servo_pulsewidth(servo_gpio,SERVO_LEFT)


        elif line == "4":
            speed_left = speed_right = 0.5
            pi.set_servo_pulsewidth(servo_gpio,SERVO_CENTER)
      

        # Apply motor speeds
        kit.motor1.throttle = speed_left
        kit.motor2.throttle = speed_right
                                                                                           
finally:
    pi.set_servo_pulsewidth(servo_gpio, 0)  # Stop servo
    pi.stop()  # Disconnect pigpio



