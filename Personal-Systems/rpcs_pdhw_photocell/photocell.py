import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_PHOTOCELL = 27
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_PHOTOCELL, GPIO.IN)

def read_photocell():
    if (GPIO.input(GPIO_photocell) == 0):
        print("photocell Pressed!")
    else:
        print("photocell Not Pressed")

if __name__ == '__main__':
    try:
        while True:
            read_photocell()            
            time.sleep(0.05)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()