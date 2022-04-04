import time
from LightControl import *

def accessibilityLight():
    light = Lights('COM4')
    light.set_enable(True)
    light.set_on(True)
    light.set_color(255)
    light.set_flash(False)

    print("Start loop, run 10s")

    thread = threading.Thread(target = loop, args=(light, ))

    thread.start()
    time.sleep(10)


    print("Turn off Lights, on False")
    light.set_on(False)
    print("Shut off, enable false")
    light.set_enable(False)
