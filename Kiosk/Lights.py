import time
from LightControl import *


print("Set up Lights, enable, on, 255, flash")
light = Lights('COM4')
light.set_enable(True)
light.set_on(True)
light.set_color(255 << 16)
light.set_flash(True)

print("Start loop, run 10s")

thread = threading.Thread(target = loop, args=(light, ))

thread.start()
time.sleep(10)

print("Set Lights, on, 65535, no flash, run 7s")
light.set_flash(False)
light.set_color(65535)
time.sleep(7)

print("Turn off Lights, on False")
light.set_on(False)
time.sleep(5)
print("Shut off, enable false")
light.set_enable(False)




