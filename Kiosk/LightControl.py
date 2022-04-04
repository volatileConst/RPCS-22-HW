from serial import Serial
from threading import Thread
import threading
import time

class Lights():
    def __init__(self, prt):
        self.serial_port = Serial(port = prt, baudrate = 9600, timeout = 2)
        self.enable = False
        self.on = False
        self.color = 0
        self.flash = False
        self.flash_state = False
        self.cmask = 4294967295
    
    def set_enable(self, state):
        self.enable = state
        
    def set_on(self, state):
        self.on = state

    def set_color(self, color):
        self.color = color
    
    def set_flash(self, flash):
        self.flash = flash

    def toggle_flash_state(self):
        self.flash_state = not self.flash_state
    
    def write_to_light(self):
        if(self.on == True):
            if(self.flash == True):
                if(self.flash_state == True):
                    cvalue = self.color & self.cmask

                else:
                    cvalue = 0
                print("flash toggle state: ", self.flash_state)
                self.toggle_flash_state()

            else:
                cvalue = self.color & self.cmask
        else:
            cvalue = 0
        
        print("cvalue: ", cvalue, " color: ", self.color)

        self.serial_port.write(str(cvalue).encode())


def loop(light):
    while(light.enable == True):
        print("writing to light")
        light.write_to_light()
        # event.wait(1)
        time.sleep(1)
    light.set_on(False)
    light.write_to_light()


