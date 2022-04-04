# Rapid Prototyping of Computer Systems Spring 2022
# Smart City Project OnwardPGH
# Subsystem: Kiosk
# Authors: Kiosk HW team

# Program to call emergency services and record 
# a video of up to 10 minutes meant to be handed over to 
# the relevant authorities
import cv2
import time
from datetime import datetime 
from AVRecording import *

# Spawn separate threads to place a call with 911 
# (any other number for demo) and to record a video


# Video recording thread
def recVideo():
    print("Entered video rec thread...\n")
    curr_datetime = datetime.now() # current date and time
    vid_name = curr_datetime.strftime("%Y_%m_%d_%H_%M_%S")

    # Record for up to 10 minutes unless manually stopped 
    # by pressing the 'x' key
    start_AVrecording(vid_name, cam=0, mic=1, rec_time=7)
    print("Started AV rec...\n")
    # Time the camera recording. Stop recording after 
    # rec_time and save video locally.
    rec_time = 10                   # in seconds TODO enter correct time
    start_time = time.time()
    while(True):
        # Close and break the loop after pressing "x" key
        if cv2.waitKey(1) &0XFF == ord('x'):
            break
        
        # Close and break the loop after rec_time seconds
        current_time = time.time()
        elapsed_time = current_time - start_time
        print()
        print(elapsed_time)
        print()
        if elapsed_time > rec_time:
            break

    # Stop the video recording
    stop_AVrecording(vid_name)
    print("Stopped AV rec...\n")

if __name__ == '__main__':
    recVideo()
