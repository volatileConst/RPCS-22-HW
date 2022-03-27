from ctypes import sizeof
import string
import time
from datetime import datetime 
from AVRecording import *
from pynput.keyboard import Key, Listener, KeyCode
from pynput import keyboard
import sys
import sched


global started, aud_name

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('\x0e'):
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key == keyboard.KeyCode.from_char('\x0e'):
            self.key_pressed = False
        return True




def recorder():
    global started, aud_name
    if listener.key_pressed and not started:
        # Start the recording
        try:
            curr_datetime = datetime.now() # current date and time
            aud_name = curr_datetime.strftime("%Y_%m_%d_%H_%M_%S")
            start_audio_recording(aud_name, mic=0, rec_time=5)
            started = True
            print("Started audio rec...\n")

        except:
            raise

    elif not listener.key_pressed and started:
        stop_audio_recording(aud_name)
        print("Stopped audio rec...\n")
        started = False
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())



if __name__ == '__main__':
    print("Prog running...\n")
    listener = MyListener()
    listener.start()
    started = False
    print("Press and hold 'ctrl+n' key to begin recording")
    print("Release the 'ctrl+n' key to end recording")
    task = sched.scheduler(time.time, time.sleep)
    task.enter(0.1, 1, recorder, ())
    task.run()


