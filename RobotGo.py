import serial
import time
import board
import RPi.GPIO as GPIO
from checkTotem import viewTotem
from adafruit_motorkit import MotorKit

# Setup
kit = MotorKit(i2c=board.I2C())     
GPIO.setmode(GPIO.BCM)              # Setting up Broadcom Chip GPIO numbering to refer to pins on board
GPIO.setup(17, GPIO.OUT)            # Make pin GPIO17 the output (send a signal to servo)
pwm = GPIO.PWM(17, 50)              # Pulse width modulation, controls servo at pin GPI017 arms angle
pwm.start(0)                        # Start PWM with 0% duty cycle so stays in place

# Center servo
pwm.ChangeDutyCycle(10)             # Center the servo with 10% duty cycle
time.sleep(0.3)                     # Give servo time to move arms
pwm.ChangeDutyCycle(0)              # Stops sending signal to pin GPI017, stays at center

# Serial setup for Bluetooth
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=1) # Recieve commands from joystick
ser.reset_input_buffer()

# Initial motor speeds
# Can set motor speeds to any decimal value -0.5 to 1 where -0.5 is reverse direction, 0 is stop, and 1 is max speed
speed_left = 0
speed_right = 0
kit.motor1.throttle = speed_left 
kit.motor2.throttle = speed_right

# Duty cycles for servo directions
SERVO_CENTER = 8
SERVO_RIGHT = 6       
SERVO_LEFT = 10
SERVO_STOP = 0

# functions
def stopMotors():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

def setServo(direction):
    if direction == "right":
        pwm.ChangeDutyCycle(SERVO_RIGHT)
    elif direction == "left":
        pwm.ChangeDutyCycle(SERVO_LEFT)
    else:
        pwm.ChangeDutyCycle(SERVO_CENTER)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(SERVO_STOP)

def setSpeed(speedLeft, speedRight):
    speed_left = speedLeft
    speed_right = speedRight
    kit.motor1.throttle = speed_left
    kit.motor2.throttle = speed_right

def redTotem():
    speed_left = speed_right = 0.99
    pwm.ChangeDutyCycle(SERVO_CENTER)
    time.sleep(.2)
    pwm.ChangeDutyCycle(SERVO_STOP)
    time.sleep(2)

def greenTotem():
    speed_left = speed_right = 0
    pwm.ChangeDutyCycle(SERVO_CENTER)
    time.sleep(.2)
    pwm.ChangeDutyCycle(SERVO_STOP)
    time.sleep(2)

def yellowTotem():
    # Simulate turning behavior
    kit.motor1.throttle = 0.25
    kit.motor2.throttle = 0.5
    time.sleep(1)
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = 0.5
    time.sleep(1)



# Main Loop
try:
    while True:
        totem = viewTotem()
        print(totem)
        if totem != "no":
            if totem == "red":
                redTotem()
                continue
            elif totem == "green":
                greenTotem()
                continue
            elif totem == "yellow":
                # Simulate turning behavior
                yellowTotem()
                continue  
        else:
            line = ser.read().decode("utf-8").strip()
            if line == "0":
                speed_left=speed_right = 0
            elif line == "1":
                setServo("center")
                setSpeed(0.75, 0.75)
            elif line == "2":
                setServo("left")
                setSpeed(.5, .75)
            elif line == "3":
                setServo("right")
                setSpeed(.75, .5)
            elif line == "4":
                setServo("center")
                setSpeed(-.5, -.5)
            
                                                                                           
finally:
    pwm.stop()
    GPIO.cleanup()
