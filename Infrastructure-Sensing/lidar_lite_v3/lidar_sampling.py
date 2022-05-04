import lidar_lite
import time

if __name__ == '__main__':

    # initialize lidar module
    lidar = lidar_lite.lidar_lite()

    # record the starting time
    start = time.time()
    time_elapsed = 0

    # use a while loop
    while time_elapsed < 10:
        
        # update time
        time_elapsed = time.time() - start

        # get reading
        print("distance:", lidar.get_distance(), "cm")

        # sleep
        time.sleep(0.5)