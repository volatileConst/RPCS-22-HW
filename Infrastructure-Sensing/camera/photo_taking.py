import os
import datetime
from datetime import datetime
import time

cnt = 0


for i in range(10):
    now = datetime.now()
    
    cur_time_str = now.strftime("%H:%M:%S")
    
    # os.system("libcamera-still -o /home/pi/Desktop/RPCS/Infrastructure-Sensing/camera/pics/" + cur_time_str + ".jpg --immediate -n")
    os.system("raspistill --nopreview -o /home/pi/Desktop/RPCS/Infrastructure-Sensing/camera/pics/" + cur_time_str + ".jpg -ex antishake")