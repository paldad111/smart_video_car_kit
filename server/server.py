#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
from time import ctime          # Import necessary modules 
from flask import Flask, abort, request

app = Flask(__name__)
HOST = ''           
PORT = 21567
BUSNUM = 1    

# Mainpage
@app.route("/")
def mainPage():
    fd = open("webapp/main.html", "rt");
    mainhtml = fd.read()
    fd.close()
    return mainhtml

# RobotMove
@app.route("/move", methods=["PUT"])
def robotMove():
	putarg = request.args

	if "x" in putarg:
		val = putarg["x"];
		val = int(val);

		if val > 0:
			car_dir.turn_right(val);
		elif val < 0:
			car_dir.turn_left(-val);
		else:
			car_dir.home()

	if "y" in putarg:
		val = putarg["y"];
		val = int(val);

		speed = abs(val) * 10;

		if val > 0:
			motor.forward();
			motor.setSpeed(speed);
		elif val < 0:
			motor.backward();
			motor.setSpeed(speed);
		else:
			motor.ctrl(0);

	return ""

if __name__ == "__main__":
	video_dir.setup(busnum=BUSNUM)
	car_dir.setup(busnum=BUSNUM)
	# Initialize the Raspberry Pi GPIO connected to the DC motor. 
	motor.setup(busnum=BUSNUM)     
	video_dir.home_x_y()
	car_dir.home()
	try:
		app.run(debug=True, host=HOST, port=PORT)
	except KeyboardInterrupt: 
		print "interrupt"
		video_dir.home_x_y()
		car_dir.home()
