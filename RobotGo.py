import serial
from adafruit_motor import motor as Motor
import time
import board
from adafruit_motorkit import MotorKit

kit=MotorKit(i2c=board.I2C())

#serial port for bluetooth
ser = serial.Serial("/dev/rfcomm0", 9600, timeout = 1)
ser.reset_input_buffer()
#set up motor
speedLeft =0
speedRight =0
kit.motor1.throttle=speedLeft
kit.motor2.throttle=speedRight
while True:
	line = ser.readline().decode("utf-8").rstrip()
	print(line)
	if("speed" in line):
		speedLeft = 0.75
		speedRight= 0.75
	if("right" in line):
		speedLeft = 0.0
		speedRight = 0.5
	if("left" in line):
		speedLeft = 0.5
		speedRight = 0.0
	if("slow" in line):
		speedLeft = 0.2
		speedRight = 0.2
	kit.motor1.throttle=speedLeft
	kit.motor2.throttle=speedRight
