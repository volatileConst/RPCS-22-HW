import os
import sys

script_dir     = os.path.dirname(__file__)
buzzer_dir     = os.path.join(script_dir, 'buzzer')
ultrasonic_dir = os.path.join(script_dir, 'HC-SR04')
IMU_dir        = os.path.join(script_dir, 'LSM6DS33')
button_dir     = os.path.join(script_dir, 'rpcs_pdhw_button')
photocell_dir  = os.path.join(script_dir, 'rpcs_pdhw_photocell')
gps_dir        = os.path.join(script_dir, 'rpcs_pdhw_gps')
aws_dir        = os.path.join(script_dir, 'cloud')

sys.path.append(buzzer_dir)
sys.path.append(ultrasonic_dir)
sys.path.append(IMU_dir)
sys.path.append(button_dir)
sys.path.append(photocell_dir)
sys.path.append(gps_dir)
sys.path.append(aws_dir)

#peripheral imports
import buzzer
import ultrasonic
from MinIMU_v5_pi import MinIMU_v5_pi
import button
import photocell
import gps

#cloud imports
import aws
import dynamoDB
import locationService
import botocore
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO PIN MACROS
GPIO_BUZZER  = 4
GPIO_TRIGGER = 27
GPIO_ECHO    = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

BUCKET_NAME         = '18745-personal-device'
FILE_PATH_REF_START = 'TODO:get loc/start'
FILE_PATH_REF_END   = 'TODO:get loc/end'
DOWNLOAD_DIR        = 'cue/dummy'

if __name__ == '__main__':

    IMU = MinIMU_v5_pi()
    IMU.enableAccel_Gyro(0,0)
    aws_obj = aws.AWS()
    gps.initGPS()

    file_iteration = 0

    while True:
        
        start, end = 0, 0
        
        # next start, end files that cue the process to start
        FILE_PATH_START = FILE_PATH_REF_START + str(file_iteration)
        FILE_PATH_END   = FILE_PATH_REF_END   + str(file_iteration)

        # wait for the software cue - 'start' file to show
        # up on aws - triggered by pd software team
        while (start == 0):
            try:
                start = download_file(BUCKET_NAME, FILE_PATH_START, DOWNLOAD_DIR)
            except botocore.exceptions.DataNotFoundError:
                continue
    
        # user is traveling
        while (end == 0):
            # get current gps
            lat, long        = gps.getLatLong()                

            # check if user entered dangerous location
            dynamoDB.checkInGeofence(lat, long)

            # get the rest of measurements
            accX, accY, accZ = IMU.readAccelerometer()
            gX, gY, gZ       = IMU.readGyro()
            dist             = distance()
            row = [lat, long, accX, accY, accZ, gX, gY, gZ, dist]

            # upload the current item on the cloud for 
            # data-analysis to later mark the condition of the road
            dynamoDB.putSingleItem(row)
            
            # user marked dangerous location - update dangerous locations
            if button.button_pressed():
                client.putGeofence(lat, long)

            # poll if user finished trip
            try:
                end = download_file(BUCKET_NAME, FILE_PATH_END, DOWNLOAD_DIR)
            except botocore.exceptions.DataNotFoundError:
                continue

            # user entered a dangerous location - buzz the buzzer
            if inGeofence(lat, long):
                buzzer.buzz()                    

            # sleep for 0.1 seconds
            #TODO: check if 0.1 sleeping achieved between invocations
            sleep(0.1)
        
        # increment file_increment for next trip
        file_increment += 1
