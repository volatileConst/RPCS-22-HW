from ctypes import sizeof
import string
import time
from datetime import datetime 
from AVRecording import *
from pynput.keyboard import Key, Listener, KeyCode
from pynput import keyboard
import sys
import sched
import win32com.client
import pythoncom


global started, aud_name

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('\x02'):
            self.key_pressed = True
        if key == keyboard.KeyCode.from_char('\x03'):
            quit()
        return True

    def on_release(self, key):
        if key == keyboard.KeyCode.from_char('\x02'):
            self.key_pressed = False
        return True



def recorder():
    global started, aud_name
    if listener.key_pressed and not started:
        # Start the recording
        try:
            curr_datetime = datetime.now() # current date and time
            aud_name = curr_datetime.strftime("%Y_%m_%d_%H_%M_%S")
            speaker = win32com.client.Dispatch("SAPI.SpVoice", pythoncom.CoInitialize())
            speaker.Speak("Please record your message!")
            start_audio_recording(aud_name, mic=0, rec_time=5)
            started = True
            print("Started audio rec...\n")

        except:
            raise

    elif not listener.key_pressed and started:
        stop_audio_recording(aud_name)
        print("Stopped audio rec...\n")
        speaker = win32com.client.Dispatch("SAPI.SpVoice", pythoncom.CoInitialize())
        speaker.Speak("Thank you for your feedback!")
        started = False
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())



if __name__ == '__main__':
    print("Prog running...\n")
    listener = MyListener()
    listener.start()
    started = False
    print("Press and hold 'ctrl+b' key to begin recording")
    print("Release the 'ctrl+b' key to end recording")
    task = sched.scheduler(time.time, time.sleep)
    task.enter(0.1, 1, recorder, ())
    task.run()


