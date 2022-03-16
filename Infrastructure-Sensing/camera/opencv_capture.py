import cv2
import time

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

for i in range(10):

    ret, frame = camera.read()
    # print(cv2.CAP_PROP_BUFFERSIZE)
    camera.grab()



    # Filename
    filename = 'sample' + str(i) + '.jpg'
      
    # Using cv2.imwrite() method
    # Saving the image
    cv2.imwrite(filename, frame)
    
    time.sleep(1)
    
exit()

while(True):
    # Capture and display photo every 5 seconds
    ret, frame = camera.read()
    # print(cv2.CAP_PROP_BUFFERSIZE)
    camera.grab()
    
    cv2.imshow('Photo', frame)
    cv2.waitKey(1000)
    # time.sleep(3)
    
    # cv2.destroyAllWindows()