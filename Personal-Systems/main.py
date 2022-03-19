#import RPi.GPIO as GPIO
import time
import os
import sys
import csv

script_dir     = os.path.dirname(__file__)
buzzer_dir     = os.path.join(script_dir, 'buzzer')
ultrasonic_dir = os.path.join(script_dir, 'HC-SR04')
IMU_dir        = os.path.join(script_dir, 'LSM6DS33')
button_dir     = os.path.join(script_dir, 'rpcs_pdhw_button')
photocell_dir  = os.path.join(script_dir, 'rpcs_pdhw_photocell')
gps_dir        = os.path.join(script_dir, 'rpcs_pdhw_gps')

aws_dir        = os.path.join(script_dir, 'cloud_data')


sys.path.append(buzzer_dir)
sys.path.append(ultrasonic_dir)
sys.path.append(IMU_dir)
sys.path.append(button_dir)
sys.path.append(photocell_dir)
sys.path.append(gps_dir)
sys.path.append(aws_dir)

#import buzzer
#import ultrasonic
#from MinIMU_v5_pi import MinIMU_v5_pi

#import button
#import photocell
#import gps
import aws
 
#GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)
 
#GPIO PIN MACROS
GPIO_BUZZER = 4
GPIO_TRIGGER = 27
GPIO_ECHO = 17
 
#set GPIO direction (IN / OUT)
#GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
#GPIO.setup(GPIO_ECHO, GPIO.IN)

BUCKET_NAME = '18745-personel-device'
FILE_PATH   = 'test.csv'

if __name__ == '__main__':

    #IMU = MinIMU_v5_pi()

    #IMU.enableAccel_Gyro(0,0)

    aws_obj = aws.AWS()

    try:
        while True:
            #dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            time.sleep(10)
            #buzzer.buzz()
            #print IMU.readAccelerometer()
            
            f = open(FILE_PATH,'w')
            writer = csv.writer(f)
            row = [1,2]
            writer.writerow(row)
            s3_msg = aws_obj.upload_file_to_bucket(BUCKET_NAME, FILE_PATH)
            print(s3_msg)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        #GPIO.cleanup()
