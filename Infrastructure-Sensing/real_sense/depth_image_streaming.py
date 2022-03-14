# This script loads a video stream on realsense camera,
# captures the frame and saves it on local folder.

# RPCS Infrastructure Sensing HW

import pyrealsense2.pyrealsense2 as rs
import numpy as np
import time
import cv2

# define a helper function to start realsense pipeline
def stream_init():

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    # Check if the camera has RGB color channels set up
    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        return None

    # Enable depth image streaming
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

    # Enable color image streaming
    if device_product_line == 'L500':
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 15)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)

    # Start streaming
    pipeline.start(config)

    return pipeline

# define a helper function to get a frame from the streaming pipeline
# index is the index of image
def get_image(pipeline, index):

    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    while not depth_frame or not color_frame:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    color_img_path_name = './image/color_map_' + str(index) + '.png'
    print(color_img_path_name)
    depth_img_path_name = './image/depth_map_' + str(index) + '.png'
    print(depth_img_path_name)

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        return (resized_color_image, depth_colormap)
    else:
        return (color_image, depth_colormap)

# setting the initial time
seconds = time.time()
time_elapsed = 0
index = 0

# main function
if __name__ == '__main__':

    # initialize pipeline
    pipeline = stream_init()

    while time_elapsed < 10:
        
        # calculate the time
        time_elapsed = time.time() - seconds
        print(time_elapsed)

        # capture an image
        get_image(pipeline, index)

        index = index + 1

        # sleep for 0.5 seconds
        time.sleep(1.0)

    # Stop streaming
    pipeline.stop()
