import numpy as np
from aws import *
import os
import cv2

# define the name of bucket here
bucket_name = "18745-infrastructure"
outer_file_path = "dummy_npz/outer_test_0.npz"
outer_dst_path = "outer_test_0.npz"
inner_file_path = "dummy_npz/inner_test_0.npz"
inner_dst_path = "inner_test_0.npz"

if __name__=='__main__':

    aws = AWS()

    # get one outer pack from cloud
    s3_msg = aws.download_file_from_bucket(bucket_name, outer_file_path, outer_dst_path)
    print(s3_msg)

    # get one inner pack from cloud
    s3_msg = aws.download_file_from_bucket(bucket_name, inner_file_path, inner_dst_path)
    print(s3_msg)

    test = np.load(outer_dst_path)

    color_map = test['RGB']

    cv2.imshow('color_map', color_map)
    cv2.waitKey(0)

    depth_map = test['DEP']

    cv2.imshow('depth_map', depth_map)
    cv2.waitKey(0)

    lidar_readings = test['PRX']

    mpu_data = test['MPU']
    print('IMU data:', mpu_data)

    mic = test['MIC']
    print('MIC data:', mic)

    for reading in lidar_readings:
        print('distance:', reading, 'cm')

    inner_test = np.load(inner_dst_path)

    cam_image = inner_test['CAM']

    cv2.imshow('cam image', cam_image)
    cv2.waitKey(0)

    gps_tuple = inner_test['GPS']

    print("latitude:", gps_tuple[0])
    print("longitude:", gps_tuple[1])

    os.remove(outer_dst_path)
    os.remove(inner_dst_path)


