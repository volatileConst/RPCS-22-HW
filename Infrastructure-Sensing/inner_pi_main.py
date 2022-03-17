# The streaming pipeline for raspberry inside
# This pipeline contains:
# - Arducam camera
# - MPU6050 IMU
# - I2S microphone
# - ZOE-M8Q GPS
# Data types include:
# - 1980 x 1080 color image
# - 6-axis data of 25 samples
# - array of audio data (1 second)
# - tuple of GPS latitude/longitude with corresponding errors

# import files with functions to sample sensor data
# from time import sleep
import numpy as np
from camera.opencv_capture import * 
from mpu.mpu_driver import *
from microphone.i2smic.i2smic_script import *
# from GPS.file.py import *
from aws import *

# define the name of bucket here
bucket_name = "18745-infrastructure"
folder_path = "dummy_npz/"

if __name__ == '__main__':
    # starting aws instance
    aws = AWS()

    # wait
    # time.sleep(3)

    # send 20 packets
    index = 0
    while index < 20:
        # sample Arducam - one sample per packet
        camera_sample = sample_camera()

        # sample MPU - 25 MPU samples per packet
        MPU_samples = run_mpu(25)

        # sample microphone - 1 second of audio per packet
        mic_samples = mic_read(1)

        # sample GPS - 1 sample per packet
        # GPS_samples = sample_GPS()

        # zip file name
        zip_path = 'inner_test_' + str(index) + '.npz'
        file_path = folder_path + 'inner_test_' + str(index) + '.npz'

        # numpy zip them
        np.savez(zip_path, CAM=camera_sample, MPU=MPU_samples, MIC=mic_samples)#, GPS=GPS_samples)
        # np.savez(zip_path, MIC=mic_samples)
        # np.savez(zip_path, CAM=camera_sample)
        # np.savez(zip_path, MPU=MPU_samples)

        # grab the file and ship it to the bucket
        s3_msg = aws.upload_file_to_bucket(bucket_name, file_path)

        index += 1

    # end of transmission
