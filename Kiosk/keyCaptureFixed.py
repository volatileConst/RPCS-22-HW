from audioCapture import *
from emergencyServices import *
from accessibility import *
from pynput import keyboard

def on_activate_m():
    print('<ctrl>+<alt>+m pressed')
    recAudio()
    print("Audio rec thread complete...\n")

def on_activate_n():
    print('<ctrl>+<alt>+n')
    emergencyServices()

def on_activate_h():
    print('<ctrl>+<alt>+h pressed')
    accessibilityLight()

def on_activate_i():
    print('<ctrl>+<alt>+i pressed')
    quit()

if __name__ == '__main__':
    print("Prog running...\n")
    
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+m': on_activate_m,
        '<ctrl>+<alt>+n': on_activate_n,
        '<ctrl>+<alt>+h': on_activate_h,
        '<ctrl>+<alt>+i': on_activate_i}) as h:
        h.join()