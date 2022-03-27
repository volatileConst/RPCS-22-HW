from audioCapture import *
from pynput import keyboard


def on_activate_m():
    print('<ctrl>+<alt>+m pressed')
    recAudio()
    print("Audio rec thread complete...\n")


def on_activate_i():
    print('<ctrl>+<alt>+i pressed')
    quit()

if __name__ == '__main__':
    print("Prog running...\n")
    
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+m': on_activate_m,
        '<ctrl>+<alt>+i': on_activate_i}) as h:
        h.join()