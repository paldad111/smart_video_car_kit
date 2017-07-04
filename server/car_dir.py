#!/usr/bin/env python
import PCA9685 as servo
import time                # Import necessary modules

MinPulse = 200
MaxPulse = 700

def Map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setup(busnum=None):
	global Rmax, Lmax, homePWM, pwm
#	leftPWM = 400
	homePWM = 450
#	rightPWM = 500
	offset =0
	try:
		for line in open('config'):
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
	except:
		print 'config error'

	Rmax = MaxPulse + offset
	Lmax = MinPulse + offset
	homePWM = (Rmax + Lmax) / 2
#	leftPWM += offset
#	homePWM += offset
#	rightPWM += offset
	if busnum == None:
		pwm = servo.PWM()                  # Initialize the servo controller.
	else:
		pwm = servo.PWM(bus_number=busnum) # Initialize the servo controller.
	pwm.frequency = 60

# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the 
# car turn left.
# ==========================================================================================
def turn_left(absv):
	global Lmax, homePWM
	val = homePWM - (homePWM - Lmax) * absv / 10
	print "pwm val: ", val
	pwm.write(0, 0, val)
#	global leftPWM
#	pwm.write(0, 0, leftPWM)  # CH0

# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right(absv):
	global Rmax, homePWM
	val = homePWM + (Rmax - homePWM) * absv / 10
	print "pwm val: ", val
	pwm.write(0, 0, val)
#	global rightPWM
#	pwm.write(0, 0, rightPWM)

# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
	angle = Map(angle, 0, 255, leftPWM, rightPWM)
	pwm.write(0, 0, angle)

def home():
	global homePWM
	pwm.write(0, 0, homePWM)

def calibrate(x):
	pwm.write(0, 0, 450+x)

def test():
	while True:
		turn_left()
		time.sleep(1)
		home()
		time.sleep(1)
		turn_right()
		time.sleep(1)
		home()

if __name__ == '__main__':
	setup()
	home()


