import RPi.GPIO as GPIO
import time
import csv
import os
import sys
from cloud import aws
from cloud import dynamoDB
from threading import Thread

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)


script_dir     = os.path.dirname(__file__)
IMU_dir        = os.path.join(script_dir, 'LSM6DS33')
button_dir     = os.path.join(script_dir, 'rpcs_pdhw_button')
gps_dir        = os.path.join(script_dir, 'rpcs_pdhw_gps')
aws_dir        = os.path.join(script_dir, 'cloud')

sys.path.append(IMU_dir)
sys.path.append(button_dir)
sys.path.append(gps_dir)
sys.path.append(aws_dir)

from MinIMU_v5_pi import MinIMU_v5_pi
import button, gps

#cloud imports
import aws
import dynamoDB
import locationService
import botocore

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
TEST_FILE_PATH = '/home/pi/RPCS-22-HW/Personal-Systems/test_file.csv'
TEST_FILE = 'test_file.csv'

#For Button
#set GPIO Pins
GPIO_BUTTON = 27

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_BUTTON, GPIO.IN)

BUCKET_NAME         = '18745-personal-device'
FILE_PATH_REF_START = 'collection/start'
FILE_PATH_REF_END   = 'collection/end'
DOWNLOAD_DIR        = 'cue/dummy'

###### edit constants here ######

#for button
def button_pressed():
    return GPIO.input(GPIO_BUTTON) == 0
	
#For Buzzer
GPIO_BUZZER = 4

#Set GPIO direction
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

#Function to buzz once

def buzz():
    for i in range(0,80):
        GPIO.output(GPIO_BUZZER, True)
        time.sleep(0.001)
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(0.001)

    for i in range(0,100):
        GPIO.output(GPIO_BUZZER, True)
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(0.002)

#For Photocell
channel = AnalogIn(mcp, MCP.P0)

LIGHT_BOUND = 17733

#For Ultrasonic
#GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
start, end = 0, 0

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

def brightness():
    value = channel.value / LIGHT_BOUND

    if value < 1:
        return 1
    elif value < 2:
        return 2
    else:
        return 3

def get_end():
    global end
    while traveling:
        try:
            end = aws_obj.download_file(BUCKET_NAME, FILE_PATH_END, DOWNLOAD_DIR)
        except botocore.exceptions.ClientError:
            end = 0

def buzz_inside_geofence():
    while traveling:
        # user entered a dangerous location - buzz the buzzer
        # TODO: implement this locationService thing
        if (True):
            buzz()

if __name__ == '__main__':
    global traveling

    IMU = MinIMU_v5_pi()
    IMU.enableAccel_Gyro(0,0)
    aws_obj = aws.AWS()
    gps.initGPS()

    file_iteration = 0
    traveling = 0
    inside_geofence = 0

    # wait for gps to warm up
    time.sleep(3)

    t = Thread(target = get_end)
    t2 = Thread(target = buzz_inside_geofence)

    while True:
        
        # next start, end files that cue the process to start
        FILE_PATH_START = FILE_PATH_REF_START + str(file_iteration)
        FILE_PATH_END   = FILE_PATH_REF_END   + str(file_iteration)

        # wait for the software cue - 'start' file to show
        # up on aws - triggered by pd software team
        while (start == 0):
            try:
                start = aws_obj.download_file(BUCKET_NAME, FILE_PATH_START, DOWNLOAD_DIR)
            except botocore.exceptions.ClientError:
                start = 0

        traveling = 1        
        t.start()
        t2.start()

        # user is traveling
        while (end == 0):

            # get current gps
            gps_valid, lat, long = gps.getGPS()

            # check if user entered dangerous location
            # TODO: change True to gps_valid
            if (True):
                locationService.checkInGeofence(lat, long)

            # get the rest of measurements
            accX, accY, accZ = IMU.readAccelerometer()
            gX, gY, gZ       = IMU.readGyro()
            dist             = distance()
            bright           = brightness()

            row = [gps_valid, lat, long, accX, accY, accZ, gX, gY, gZ, dist, bright]

            print(row)

            # upload the current item on the cloud for 
            # data-analysis to later mark the condition of the road
            dynamoDB.putSingleItem(row)

            # user marked dangerous location - update dangerous locations
            if button.button_pressed():
                locationService.putGeofence(lat, long)

            # sleep for 0.1 seconds
            #TODO: check if 0.1 sleeping achieved between invocations
            time.sleep(0.1)

            # background thread polls for user ending trip
        
        # increment file_increment for next trip
        file_increment += 1
        traveling = 0
        t.join()
        t2.join()

        start, end = 0, 0
