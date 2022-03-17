import cv2
import time

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
width = 1920
height = 1080
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

"""for i in range(10):

    ret, frame = camera.read()
    camera.grab()
    filename = 'sample' + str(i) + '.jpg'
    image = cv2.resize(frame, (680, 480))
    cv2.imshow(filename, image)
    cv2.waitKey(1000)
    # time.sleep(2)
    
exit()"""

def sample_camera():
    ret, frame = camera.read()
    camera.grab()
    print("Photo taken!")

    return frame
    
    # cv2.destroyAllWindows()

"""while(True):
    # Capture and display photo every 5 seconds
    ret, frame = camera.read()
    # print(cv2.CAP_PROP_BUFFERSIZE)
    camera.grab()
    
    image = cv2.resize(frame, (680, 480))
    cv2.imshow('photo', image)
    cv2.waitKey(1000)
    # time.sleep(3)
    
    # cv2.destroyAllWindows()"""
