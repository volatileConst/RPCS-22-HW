import RPi.GPIO as GPIO
from time import sleep

# Macros for mic sensor
MIC_DIG_GPIO = 17
MIC_ANA_GPIO = 27

# Initialize mic
def mic_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MIC_DIG_GPIO, GPIO.IN)
    GPIO.setup(MIC_ANA_GPIO, GPIO.IN)

def mic_read_digital():
    input_value = GPIO.input(MIC_DIG_GPIO)
    return input_value

def mic_read_analog():
    input_value = GPIO.input(MIC_ANA_GPIO)
    return input_value

mic_init()
while(1):
    digital_value = mic_read_digital()
    analog_value = mic_read_analog()
    print(digital_value, analog_value)
    sleep(1)