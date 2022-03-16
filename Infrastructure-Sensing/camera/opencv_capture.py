import cv2
import time

camera = cv2.VideoCapture(0)

while(True):
    # Capture and display photo every 5 seconds
    ret, frame = camera.read()
    cv2.imshow('Photo', frame)
    cv2.waitKey(1000)
    time.sleep(1.5)