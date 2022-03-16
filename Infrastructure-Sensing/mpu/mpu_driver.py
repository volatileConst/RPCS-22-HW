# motion processor unit (mpu) driver implementation
# https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
import smbus
import numpy
from time import sleep

# Macros
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def hi():
	print("hi")
	
# Initialize MPU
def mpu_init(bus, Device_Address):
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def mpu_read_data(bus, Device_Address):
	#Accelero and Gyro value are 16-bit
	high = bus.read_byte_data(Device_Address, addr)
	low = bus.read_byte_data(Device_Address, addr+1)

	#concatenate higher and lower value
	value = ((high << 8) | low)
	
	#to get signed value from mpu6050
	if(value > 32768):
			value = value - 65536
	return value

def run_mpu():
	bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
	Device_Address = 0x68   # MPU6050 device address

	mpu_init(bus, Device_Address)

	print ("Reading Data of Gyroscope and Accelerometer")


	res_array = numpy.array([])

	while True:
		gx_arr = []
		gy_arr = []
		gz_arr = []
		ax_arr = []
		ay_arr = []
		az_arr = []
		for x in range(100):
			#Read Accelerometer raw value
			acc_x = mpu_read_data(ACCEL_XOUT_H)
			acc_y = mpu_read_data(ACCEL_YOUT_H)
			acc_z = mpu_read_data(ACCEL_ZOUT_H)
			
			#Read Gyroscope raw value
			gyro_x = mpu_read_data(GYRO_XOUT_H)
			gyro_y = mpu_read_data(GYRO_YOUT_H)
			gyro_z = mpu_read_data(GYRO_ZOUT_H)
			
			#Full scale range +/- 250 degree/C as per sensitivity scale factor
			Ax = acc_x/16384.0
			Ay = acc_y/16384.0
			Az = acc_z/16384.0
			
			Gx = gyro_x/131.0
			Gy = gyro_y/131.0
			Gz = gyro_z/131.0

			# Store sample data into array and average it
			gx_arr += [Gx]
			gy_arr += [Gy]
			gz_arr += [Gz]
			ax_arr += [Ax]
			ay_arr += [Ay]
			az_arr += [Az]

			sleep(0.001)
		
		Gx = sum(gx_arr) / len(gx_arr)
		Gy = sum(gy_arr) / len(gy_arr)
		Gz = sum(gz_arr) / len(gz_arr)
		Ax = sum(ax_arr) / len(ax_arr)
		Ay = sum(ay_arr) / len(ay_arr)
		Az = sum(az_arr) / len(az_arr)

		res = (Gx, Gy,Gz,Ax,Ay,Az)

		numpy.append(res_array, res)

		print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
