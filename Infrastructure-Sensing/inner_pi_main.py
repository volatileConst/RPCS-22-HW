# runs on the RPi inside of the car
# samples sensor data and compresses data into a package to send to cloud
# aiming to send a package once every 5 seconds
# sensor sampling + compression needs to happen in that time frame
# note that this file is WIP - will not run properly yet (as of 3-16-22)

# import files with functions to sample sensor data
import time
import numpy as np
# from camera/file.py import * 
# from mpu/file.py import *
from microphone.mpu_driver.py import *
# from GPS/file.py import *

# setup sensors as needed
def initialize_sensors():
    # call functions
    mpu_init()

if __name__ = '__main__':
    # start sensors
    initialize_sensors()

    while true:
        # sample Arducam - one sample per package
        camera_sample = sample_camera()

        # sample MPU - 50 MPU samples per package
        MPU_samples = mpu_read_data()

        # sample microphone - 1 second of audio per package
        microphone_samples = sample_mic()

        # sample GPS - 1 sample per package
        GPS_samples = sample_GPS()

        # compress data samples and send to AWS

