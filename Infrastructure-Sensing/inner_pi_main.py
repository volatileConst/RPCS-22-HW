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
import time
import numpy as np
import _thread
from camera.opencv_capture import * 
# from mpu.mpu_driver import *
from microphone.i2smic.i2smic_script import *
# from GPS.file.py import *
from aws import *


# define the name of bucket here
bucket_name = "18745-infrastructure"
folder_path = "dummy_npz/"
mic_dev_num = mic_init()
mic_time = 1
collect_index = 0
send_index = 0
# starting aws instance
aws = AWS()


def sensors_read():
    print("start taking photos...")
    start = time.time()
    camera_sample = sample_camera()
    end = time.time()
    print("Photo taken within " + str(end-start) + " seconds!")

    # # sample MPU - 25 MPU samples per packet
    # print("start collecting mpu data...")
    # start = time.time()
    # MPU_samples = run_mpu(25)
    # end = time.time()
    # print("mpu data collected within " + str(end-start) + " seconds!")


    # sample microphone - 1 second of audio per packet
    start = time.time()
    mic_samples = mic_read(mic_dev_num, mic_time)
    end = time.time()
    print("Audio recorded within " + str(end-start) + " seconds!")


    # # sample GPS - 1 sample per packet
    # print("start collecting gps data...")
    # start = time.time()
    # GPS_samples = sample_GPS()
    # end = time.time()
    # print("gps data collected within " + str(end-start) + " seconds!")
    
    # zip file name
    zip_path = 'inner_test_' + str(collect_index) + '.npz'
    file_path = folder_path + 'inner_test_' + str(collect_index) + '.npz'

    # numpy zip them
    start = time.time()
    np.savez(zip_path, CAM=camera_sample, MIC=mic_samples)
    end = time.time()
    print("Pkt created within " + str(end-start) + " seconds!")

def send_data():
    global aws
    zip_path = 'inner_test_' + str(send_index) + '.npz'
    file_path = folder_path + 'inner_test_' + str(send_index) + '.npz'

    # grab the file and ship it to the bucket
    start = time.time()
    s3_msg = aws.upload_file_to_bucket(bucket_name, file_path)
    end = time.time()
    print("Pkt sent within " + str(end-start) + " seconds!")

def send_data_wrapper():
    global send_index
    global collect_index
    while (1):
        if (send_index >= collect_index):
            print("[sending thread]Waiting for new pkts!!! Sleep for 5 seconds...")
            # time.sleep(5)
        else:
            print("[sending thread]Seding data to the database!")
            send_data()
            send_index += 1


def sensors_read_wrapper():
    global collect_index
    while (1):
        sensors_read()
        collect_index += 1

if __name__ == '__main__':

    _thread.start_new_thread(sensors_read_wrapper, ())
    _thread.start_new_thread(send_data_wrapper, ())
    while (1):
        time.sleep(1)
        print(collect_index)
        print(send_index)

    # # send packets
    # index = 0
    # while index < 5:
    #     # sample Arducam - one sample per packet
    #     print("start taking photos...")
    #     start = time.time()
    #     camera_sample = sample_camera()
    #     end = time.time()
    #     print("Photo taken within " + str(end-start) + " seconds!")

    #     # # sample MPU - 25 MPU samples per packet
    #     # print("start collecting mpu data...")
    #     # start = time.time()
    #     # MPU_samples = run_mpu(25)
    #     # end = time.time()
    #     # print("mpu data collected within " + str(end-start) + " seconds!")


    #     # sample microphone - 1 second of audio per packet
    #     start = time.time()
    #     mic_samples = mic_read(mic_dev_num, mic_time)
    #     end = time.time()
    #     print("Audio recorded within " + str(end-start) + " seconds!")


    #     # # sample GPS - 1 sample per packet
    #     # print("start collecting gps data...")
    #     # start = time.time()
    #     # GPS_samples = sample_GPS()
    #     # end = time.time()
    #     # print("gps data collected within " + str(end-start) + " seconds!")

    #     # zip file name
    #     zip_path = 'inner_test_' + str(index) + '.npz'
    #     file_path = folder_path + 'inner_test_' + str(index) + '.npz'

    #     # numpy zip them
    #     # np.savez(zip_path, CAM=camera_sample, MPU=MPU_samples, MIC=mic_samples)#, GPS=GPS_samples)
    #     start = time.time()
    #     np.savez(zip_path, CAM=camera_sample, MIC=mic_samples)#, GPS=GPS_samples)
    #     end = time.time()
    #     print("Pkt created within " + str(end-start) + " seconds!")

    #     # np.savez(zip_path, MIC=mic_samples)
    #     # np.savez(zip_path, CAM=camera_sample)
    #     # np.savez(zip_path, MPU=MPU_samples)

    #     # grab the file and ship it to the bucket
    #     start = time.time()
    #     s3_msg = aws.upload_file_to_bucket(bucket_name, file_path)
    #     end = time.time()
    #     print("Pkt sent within " + str(end-start) + " seconds!")

    #     index += 1

    # # end of transmission
