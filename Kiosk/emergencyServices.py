# Rapid Prototyping of Computer Systems Spring 2022
# Smart City Project TODO insert final name
# Subsystem: Kiosk
# Authors: Kiosk HW team

# Program to call emergency services, flash lights red 
# and record a video of up to 10 minutes meant to be 
# handed over to the relevant authorities

from videoCapture import *
from LightControl import *
import threading 
import time

# Spawn separate threads to place a call with 911 
# (any other number for demo) and to record a video

RED = 16711680  

def flashRed(vid_thread):
    print("Entered flash red thread...\n")

    # Setup lights
    light = Lights('COM4', 100)
    light.set_enable(True)
    light.set_on(True)
    light.set_color('RED')
    light.set_flash(True)
    
    thread = threading.Thread(target = loop, args=(light, ))
    thread.start()

    # Poll for recVideo completioncd
    # while (vid_thread.is_alive()):
    #     # Do nothing
    #     pass
    rec_time = 15                   # in seconds TODO enter correct time
    start_time = time.time()
    while(True):
        # Close and break the loop after pressing "x" key
        if cv2.waitKey(1) &0XFF == ord('x'):
            break
        
        # Close and break the loop after rec_time seconds
        current_time = time.time()
        elapsed_time = current_time - start_time
        # print()
        # print(elapsed_time)
        # print()
        if elapsed_time > rec_time:
            break

    light.set_on(False)
    light.set_enable(False)


def emergencyServices():

    # Create threads
    print("entered here \n")
    # thread_call = threading.Thread(target=placeCall)
    thread_video = threading.Thread(target=recVideo) # Start recording video
    thread_lights = threading.Thread(target=flashRed, args=(thread_video, )) # Start flashing lights red

    # Start Threads
    # thread_call.start()
    thread_video.start()
    thread_lights.start()

    # Join Threads
    # thread_call.join()
    thread_lights.join()
    thread_video.join()
    
if __name__ == '__main__':
    emergencyServices()

