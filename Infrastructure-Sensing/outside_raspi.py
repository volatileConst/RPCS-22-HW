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
from real_sense.depth_image_streaming import *
from lidar_lite_v3.lidar_lite import *



if __name__ == '__main__':
    
    # starting realsense pipeline
    pipeline = stream_init()

    # initialize a lidar instance
    lidar = lidar_lite()

    # sleep for 5 seconds, wait for camera and lidar to be ready
    time.sleep(5)

    # indexing the file
    index = 0
    
    while index < 3:

        # getting color/depth maps from real sense
        color_map, depth_map = get_image(pipeline, index)

        # getting lidar reading
        distance = lidar.get_distance()

        # zip file name
        zip_path = './dummy_npz/outer_test_' + str(index) + '.npz'

        # numpy zip them
        np.savez(zip_path, RGB=color_map, DEP=depth_map, PRX=distance)

        index += 1

    # stop the pipeline
    pipeline.stop()