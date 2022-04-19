import RPi.GPIO as GPIO
import time
import csv
import os
import sys
import aws

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
FLAT              = 1  # 1 ~ 5
MID               = 2
NOT_FLAT          = 3  # dummy value for bumps - need to manually label looking at data graph
NO_BUMP_PATHNAME  = '/home/pi/RPCS-22-HW/Personal-Systems/flat_campus_grass.csv'
YES_BUMP_PATHNAME = '/home/pi/RPCS-22-HW/Personal-Systems/bump1.csv'
NUM_SAMPLES       = 5000
FLAT_LIBRARY      = '/home/pi/RPCS-22-HW/Personal-Systems/wheelchair_flat_library.csv'
BUMPY_LIBRARY     = '/home/pi/RPCS-22-HW/Personal-Systems/wheelchair_bumpy_library.csv'
FLAT_GRAVEL       = '/home/pi/RPCS-22-HW/Personal-Systems/wheelchair_flat_gravel.csv'
MID_RED_GRAVEL_PATH    = '/home/pi/RPCS-22-HW/Personal-Systems/wheelchair_mid_red_gravel.csv'
MID_RED_GRAVEL_FILE  = 'wheelchair_mid_red_gravel.csv' 
CLOUD_TEST        = '/home/pi/RPCS-22-HW/Personal-Systems/PDHW_Test_file.csv'

#For Button
#set GPIO Pins
GPIO_BUTTON = 27

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_BUTTON, GPIO.IN)

BUCKET_NAME = "18745-personal-device"
###### edit constants here ######


#for button
def button_pressed():
    return GPIO.input(GPIO_BUTTON) == 0
	
    
#For Ultrasonic
#GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
	
	

if __name__ == "__main__":	
    while True:
        if button.button_pressed():
            #f = open(NO_BUMP_PATHNAME, 'w')
            f = open(MID_RED_GRAVEL_PATH, 'w');
            writer = csv.writer(f)


 
            AWS = aws.AWS()
            AWS.upload_file_to_bucket(BUCKET_NAME, MID_RED_GRAVEL_FILE)

            IMU = MinIMU_v5_pi()
            IMU.enableAccel_Gyro(0,0)
            gps.initGPS()
            cur_time = 0

            while cur_time < NUM_SAMPLES * SLEEPTIME:
                gps_valid, latitude, longitude = gps.getGPS()
                bumpiness = MID
                if button.button_pressed():
                    dist = distance()
                else:
                    dist = -1

                row = [round(cur_time, 1), bumpiness, IMU.readAccelerometer(), IMU.readGyro(), dist, gps_valid, latitude, longitude]
        
                writer.writerow(row)
                print(row)
        
                cur_time += SLEEPTIME
                time.sleep(SLEEPTIME)
