# The streaming pipeline for raspberry outside
# This pipeline contains:
#  - RealSense Depth Camera
#  - Lidar-Lite v3
# Data types include:
#  - depth image (640 * 480)
#  - color image (640 * 480)
#  - lidar data (integer)
#  - microphone data (numpy array for 1s audio)
#  - imu data (6 * n )

import time
import numpy as np
import os
import _thread
from real_sense.depth_image_streaming import *
from microphone.i2smic.i2smic_script import *
from lidar_lite_v3.lidar_lite import *
from aws import *
from mpu.mpu_driver import *

# commented libraries for now
# from GPS.file.py import *

# define the name of bucket here
bucket_name = "18745-infrastructure"
folder_path = "dummy_npz/"

# define mic instance and sample time
mic_dev_num = mic_init()
mic_time = 1

# define number of samples
num_samples = 5

# two global indices for threads
collect_index = 0
send_index = 0

# starting aws instance
aws = AWS()

# starting realsense pipeline
pipeline = stream_init()

# initialize a lidar instance
lidar = lidar_lite()

# define thread for all sensors to read
def sensors_read():

    # reading color and depth map from real sense
    print("taking RealSense images...")
    color_map, depth_map = get_image(pipeline, index)
    print("RealSense images taken!")

    # reading microphone data
    print("taking microphone data...")
    mic_samples = mic_read(mic_dev_num, mic_time)
    print("microphone data collected!")

    # sampling lidar data - 25 lidar samples per packet
    print("collecting lidar data...")
    lidar_samples = lidar.get_distance(25)
    print("lidar data sampled!")

    # sampling MPU data - 25 MPU samples per packet
    print("collecting mpu data...")
    MPU_samples = run_mpu(25)
    print("MPU data sampled!")

    # sample GPS data - 1 sample per packet
    # print("collecting gps data...")
    # GPS_samples = sample_GPS()
    # print("gps data sampled!")

    # zip file name
    zip_path = 'outer_test_' + str(collect_index) + '.npz'
    file_path = folder_path + 'outer_test_' + str(collect_index) + '.npz'

    # numpy zip compressed
    np.savez_compressed(zip_path, RGB=color_map, DEP=depth_map, MIC=mic_samples, PRX=lidar_samples, MPU=MPU_samples)
    print("packet zipped!")

    # commented for now
    # MPU=MPU_samples
    # GPS=GPS_samples

# define thread to ship the packet
def send_data():
    # global instances
    global aws

    file_path = folder_path + 'outer_test_' + str(send_index) + '.npz'

    # send to s3 bucket
    s3_msg = aws.upload_file_to_bucket(bucket_name, file_path)
    print("packet sent!")

# define sensor read wrapper
def sensors_read_wrapper():
    # global instances
    global collect_index
    global send_index

    # thread ends when all packets are collected
    while collect_index < num_samples:
        # interlock
        if (collect_index > send_index):
            print("[reading thread]Packet created!!! Sleep for 0.5 seconds...")
            time.sleep(0.5) # sleep to manually block the thread
        else:
            sensors_read()
            collect_index += 1

# define send data wrapper
def send_data_wrapper():
    # global instances
    global send_index
    global collect_index

    # thread ends when all packets are sent
    while send_index < num_samples:
        # interlock
        if (send_index >= collect_index):
            print("[sending thread]Waiting for new pkts!!! Sleep for 0.5 seconds...")
            time.sleep(0.5) # sleep to manually block the thread
        else:
            print("[sending thread]Seding data to the database!")
            send_data()
            send_index += 1

if __name__ == '__main__':

    # sleep for 3 seconds, wait for camera and lidar to be ready
    print("wait for sensors to initialize...")
    time.sleep(3)

    # record starting time
    # start_time = time.time()

    # start threads
    _thread.start_new_thread(sensors_read_wrapper, ())
    _thread.start_new_thread(send_data_wrapper, ())
    
    while send_index < num_samples:
        # print time
        # print("current time:", time.time() - start_time)
        time.sleep(1)
        print("packets collected:", collect_index)
        print("packets sent:", send_index)
    
    # delete packets
    index = 0

    while index < num_samples:

        zip_path = 'outer_test_' + str(index) + '.npz'
        os.remove(zip_path)
        index += 1


    # stop the pipeline
    pipeline.stop()