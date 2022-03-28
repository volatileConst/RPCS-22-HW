# The streaming pipeline for raspberry inside
# This pipeline contains:
# - Arducam camera
# - Sixfab GPS
# Data types include:
# - 1980 x 1080 color image
# - tuple of GPS latitude/longitude with corresponding errors

# import files with functions to sample sensor data
import time
import numpy as np
import _thread
from camera.opencv_capture import *
from GPS.read_Gmouse_GPS import *
from aws import *

# define the name of bucket here
aws = 0
bucket_name = "18745-infrastructure"
folder_path = "dummy_npz/"

# keep track of packets
collect_index = 0
send_index = 0

# keep track of last GPS location
last_latitude = 0
last_longitude = 0

def initialization():
    # starting AWS instance
    global aws
    aws = AWS()

    # starting connection to GPS
    initialize_GPS()

def sensors_read():
    # read camera
    print("[sensing thread] Taking photo...")
    
    start = time.time()
    camera_sample = sample_camera()
    end = time.time()

    print("[sensing thread] Photo taken within " + str(end-start) + " seconds!")

    # read GPS
    print("[sensing thread] Start collecting GPS data...")

    start = time.time()
    GPS_sample = sample_GPS()
    end = time.time()

    print("[sensing thread] GPS data collected within " + str(end-start) + " seconds!")
    
    # compress data
    zip_path = 'inner_test_' + str(collect_index) + '.npz'

    start = time.time()
    np.savez_compressed(zip_path, CAM=camera_sample, GPS=GPS_sample)
    end = time.time()

    print("[sensing thread] Packet " + str(collect_index) + " created within " + str(end-start) + " seconds!")

def send_data():
    # send the file to the bucket
    zip_path = 'inner_test_' + str(send_index) + '.npz'
    cloud_file_path = folder_path + 'inner_test_' + str(send_index) + '.npz'

    start = time.time()
    aws.upload_file_to_bucket(bucket_name, cloud_file_path)
    end = time.time()

    print("[sending thread] Packet " + str(send_index) + " sent within " + str(end-start) + " seconds!")

    # remove file from disk
    start = time.time()
    os.remove(zip_path)
    end = time.time()

    print("[sending thread] Removed packet " + str(send_index) + " from disk within " + str(end-start) + " seconds!")

def send_data_wrapper():
    global send_index

    while (1):
        if (send_index >= collect_index):
            print("[sending thread] Waiting for new packets!")
            time.sleep(1) # delay for other threads to run
        else:
            print("[sending thread] Sending data to the database!")
            send_data()
            send_index += 1

def sensors_read_wrapper():
    global collect_index

    while (1):
        sensors_read()
        collect_index += 1

if __name__ == '__main__':
    # initialize AWS and GPS
    initialization()

    # create sensing + streaming threads
    _thread.start_new_thread(send_data_wrapper, ())
    _thread.start_new_thread(sensors_read_wrapper, ())
    print("Threads spawned!")

    while (1):
        time.sleep(1) # delay for other threads to run
        # print(collect_index)
        # print(send_index)
