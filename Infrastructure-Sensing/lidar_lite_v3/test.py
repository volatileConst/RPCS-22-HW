import lidar_lite
import time

if __name__ == '__main__':

  # initialize lidar instance
  lidar = lidar_lite.lidar_lite()

  # get readings
  while True:
    print("distance: ", lidar.read_distance(), "cm")
    time.sleep(0.2)