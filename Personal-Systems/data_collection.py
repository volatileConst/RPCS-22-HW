import RPi.GPIO as GPIO
import time
import csv
import os
import sys

script_dir     = os.path.dirname(__file__)
IMU_dir        = os.path.join(script_dir, 'LSM6DS33')
button_dir     = os.path.join(script_dir, 'rpcs_pdhw_button')
gps_dir        = os.path.join(script_dir, 'rpcs_pdhw_gps')
sys.path.append(IMU_dir)
sys.path.append(button_dir)
sys.path.append(gps_dir)

from MinIMU_v5_pi import MinIMU_v5_pi
import button, gps

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

###### edit constants here ######

SLEEPTIME         = 0.1
flat              = 1  # 1 ~ 5
not_flat          = 3  # dummy value for bumps - need to manually label looking at data graph
NO_BUMP_PATHNAME  = '/home/pi/RPCS-22-HW/Personal-Systems/flat_campus_grass.csv'
YES_BUMP_PATHNAME = '/home/pi/RPCS-22-HW/Personal-Systems/bump1.csv'
NUM_SAMPLES       = 5000

#set GPIO Pins
GPIO_BUTTON = 27

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_BUTTON, GPIO.IN)

###### edit constants here ######

if __name__ == "__main__":	
	
	f = open(NO_BUMP_PATHNAME, 'w')
	writer = csv.writer(f)

	IMU = MinIMU_v5_pi()
	IMU.enableAccel_Gyro(0,0)

	gps.initGPS()

	cur_time = 0

	while cur_time < NUM_SAMPLES * SLEEPTIME: # getting hundred thousand samples

		gps_valid = gps.getGPS()

		bumpiness = 0
		if button.button_pressed():
			bumpiness = not_flat
		else:
			bumpiness = flat
		
		if gps_valid:
			row = [cur_time, bumpiness, IMU.readAccelerometer(), IMU.readGyro(), 1]
		else:
			row = [cur_time, bumpiness, IMU.readAccelerometer(), IMU.readGyro()]
		#writer.writerow(row)
		
		print(row)

		cur_time += SLEEPTIME
		time.sleep(SLEEPTIME)
