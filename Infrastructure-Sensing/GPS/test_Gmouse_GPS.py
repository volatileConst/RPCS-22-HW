# test code for this library: https://github.com/MartijnBraam/gpsd-py3

import gpsd

gpsd.connect()

while (1):
  packet = gpsd.get_current()
  print(packet.position())
  sleep(3)
