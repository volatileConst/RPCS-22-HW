from MinIMU_v5_pi import MinIMU_v5_pi
import time

def main():
	#Setup the MinIMU_v5_pi
	IMU = MinIMU_v5_pi()
	IMU.enableAccel_Gyro(0,0)

	while True: #Main loop             
		time.sleep(0.1)
		print IMU.readAccelerometer()


if __name__ == "__main__":
	main()


