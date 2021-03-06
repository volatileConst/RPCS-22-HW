# this file defines the lidar lite v3 class for RaspberryPi 4

import smbus
import time

# define bus number over here
bus_num = 3

# initialize i2c bus
bus = smbus.SMBus(bus_num)

class lidar_lite():

    def __init__(self):
        self.i2c_addr = 0x62
        self.write_reg = 0x00
        self.wait_reg = 0x01
        self.low_byte_reg = 0x10
        self.high_byte_reg = 0x0f
    
    def get_distance(self, samples):

        readings = []

        for num in range(samples):
            # 1. write 0x04 to register 0x00
            bus.write_byte_data(self.i2c_addr, self.write_reg, 0x04)

            # 2. read register 0x01 until bit 0 (LSB) goes low
            bus.write_byte(self.i2c_addr, self.wait_reg)
            while bus.read_byte(self.i2c_addr) & 0x01 != 0:
                pass

            # 3. read high byte and low byte
            bus.write_byte(self.i2c_addr, self.high_byte_reg)
            reading = bus.read_byte(self.i2c_addr) << 8
            bus.write_byte(self.i2c_addr, self.low_byte_reg)
            reading |= bus.read_byte(self.i2c_addr)

            # 4. append the reading
            readings.append(reading)

        # return all readings
        return readings