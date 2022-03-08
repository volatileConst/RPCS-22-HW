import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_BUTTON = 27
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_BUTTON, GPIO.IN)

def button_pressed():
    return GPIO.input(GPIO_BUTTON) == 0

if __name__ == '__main__':
    try:
        while True:
            read_button()            
            time.sleep(0.05)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()