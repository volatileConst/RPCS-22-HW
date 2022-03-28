# uses this library: https://github.com/MartijnBraam/gpsd-py3

import gpsd

def initialize_GPS():
    # connect to localhost
    gpsd.connect()

def sample_GPS():
    # poll GPS using gpsd
    packet = gpsd.get_current()
    print(packet.position())
    return packet.position()
