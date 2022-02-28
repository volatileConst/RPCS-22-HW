import os
import datetime
from datetime import datetime
import time

cnt = 0


for i in range(10):
    now = datetime.now()
    
    cur_time_str = now.strftime("%H:%M:%S")
    
    os.system("raspistill -vf -hf -o /home/pi/Desktop/RPCS/Infrastructure-Sensing/camera/pics/" + cur_time_str + ".jpg")