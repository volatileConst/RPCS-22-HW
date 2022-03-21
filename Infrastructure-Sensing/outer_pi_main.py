# The streaming pipeline for raspberry outside
# This pipeline contains:
#  - RealSense Depth Camera
#  - Lidar-Lite v3
# Data types include:
#  - depth image (640 * 480)
#  - color image (640 * 480)
#  - lidar data (integer)

import time
import numpy as np
import os
from real_sense.depth_image_streaming import *
from lidar_lite_v3.lidar_lite import *
from aws import *

# define the name of bucket here
bucket_name = "18745-infrastructure"
folder_path = "dummy_npz/"

# define number of samples
num_samples = 5


if __name__ == '__main__':
    
    # starting aws instance
    aws = AWS()

    # starting realsense pipeline
    pipeline = stream_init()

    # initialize a lidar instance
    lidar = lidar_lite()

    # sleep for 5 seconds, wait for camera and lidar to be ready
    time.sleep(5)

    # indexing the file
    index = 0

    # record starting time
    # start_time = time.time()
    
    while index < num_samples:
        # print time
        # print("current time:", time.time() - start_time)

        # getting color/depth maps from real sense
        color_map, depth_map = get_image(pipeline, index)

        # getting lidar reading
        distance = []
        for i in range(25):
            distance.append(lidar.get_distance())

        # zip file name
        zip_path = 'outer_test_' + str(index) + '.npz'

        file_path = folder_path + 'outer_test_' + str(index) + '.npz'

        # numpy zip them
        np.savez(zip_path, RGB=color_map, DEP=depth_map, PRX=distance)

        # grab the file and ship it to the bucket
        s3_msg = aws.upload_file_to_bucket(bucket_name, file_path)

        print("outer pi packet", index, "shipped!")

        index += 1

    # delete files
    index = 0

    while index < num_samples:

        zip_path = 'outer_test_' + str(index) + '.npz'
        os.remove(zip_path)
        index += 1


    # stop the pipeline
    pipeline.stop()