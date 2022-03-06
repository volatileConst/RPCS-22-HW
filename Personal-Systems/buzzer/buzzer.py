import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_BUZZER = 4
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

def buzz():
    for i in range(0,80):
        GPIO.output(GPIO_BUZZER, True)
        time.sleep(0.001)
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(0.001)

    for i in range(0,100):
        GPIO.output(GPIO_BUZZER, True)
        GPIO.output(GPIO_BUZZER, False)
        time.sleep(0.002)

 
if __name__ == '__main__':
    try:
        while True:
            buzz()
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()