from mpu.mpu_driver import *
from microphone.i2smic.i2smic_script import *


bus, Device_Address = mpu_init()
x = mpu_read_data(bus, Device_Address, ACCEL_XOUT_H)
mic_read(1)
