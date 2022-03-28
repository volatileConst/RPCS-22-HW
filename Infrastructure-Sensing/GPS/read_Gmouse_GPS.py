# uses this library: https://github.com/MartijnBraam/gpsd-py3

import gpsd

def initialize_gps():
    gpsd.connect()

def read_coordinates():
    # poll GPS
    packet = gpsd.get_current()
    print(packet.position())
    return packet.position()
