import RPi.GPIO as GPIO
import time
import os
import sys

script_dir     = os.path.dirname(__file__)
buzzer_dir     = os.path.join(script_dir, 'buzzer')
ultrasonic_dir = os.path.join(script_dir, 'HC-SR04')
IMU_dir        = os.path.join(script_dir, 'LSM6DS33')
button_dir     = os.path.join(script_dir, 'rpcs_pdhw_button')
photocell_dir  = os.path.join(script_dir, 'rpcs_pdhw_photocell')
gps_dir        = os.path.join(script_dir, 'rpcs_pdhw_gps')

sys.path.append(buzzer_dir)
sys.path.append(ultrasonic_dir)
sys.path.append(IMU_dir)
sys.path.append(button_dir)
sys.path.append(photocell_dir)
sys.path.append(gps_dir)

import buzzer
import ultrasonic
from MinIMU_v5_pi import MinIMU_v5_pi
import button
import photocell
import gps
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO PIN MACROS
GPIO_BUZZER = 4
GPIO_TRIGGER = 27
GPIO_ECHO = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

if __name__ == '__main__':

    IMU = MinIMU_v5_pi()
    IMU.enableAccel_Gyro(0,0)

    try:
        while True:
            #dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            buzzer.buzz()
            print IMU.readAccelerometer()

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
