import serial
from adafruit_motor import motor as Motor
import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit

kit=MotorKit(i2c=board.I2C())


GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)
p = GPIO.PWM(17,50)
p.start(0)

p.ChangeDutyCycle(7)
p.ChangeDutyCycle(0)
#serial port for bluetooth
ser = serial.Serial("/dev/rfcomm0", 9600, timeout = 1)
ser.reset_input_buffer()
#set up motor
speedLeft =0
speedRight =0
kit.motor1.throttle=speedLeft
kit.motor2.throttle=speedRight
while True:
	line = ser.read().decode("utf-8")
	print(line)
	if('1' in line):
		speedLeft = 0.75 #forward
		speedRight= 0.75
		p.ChangeDutyCycle(7)

	elif('2' in line):
		speedLeft = 0.75 #right
		speedRight = 0.5
		p.ChangeDutyCycle(11)
	elif('3' in line):
		speedLeft = 0.5 #left
		speedRight = 0.75
		p.ChangeDutyCycle(5)
	elif('4' in line):
		speedLeft = 0 #slow
		speedRight = 0
		p.ChangeDutyCycle(7)

	kit.motor1.throttle=speedLeft
	kit.motor2.throttle=speedRight
p.stop()
GPIO.cleanup()
