# Rapid Prototyping of Computer Systems Spring 2022
# Smart City Project TODO insert final name
# Subsystem: Kiosk
# Authors: Kiosk HW team

# Program to record audio feedback of a user
import pyaudio
import time
from datetime import datetime 
from AVRecording import *

def recAudio():
    
    curr_datetime = datetime.now() # current date and time
    aud_name = curr_datetime.strftime("%Y_%m_%d_%H_%M_%S")

    # Record for up to 10 minutes unless manually stopped 
    # by pressing the 'x' key
    start_audio_recording(aud_name, mic=2, rec_time=10)
    print("Started audio rec...\n")
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
        if elapsed_time > rec_time:
            break

    # Stop the video recording
    stop_audio_recording(aud_name)
    print("Stopped audio rec...\n")



if __name__ == '__main__':
    recAudio()
    print("Audio rec thread complete...\n")


