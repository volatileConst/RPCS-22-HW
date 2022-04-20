# from serial import Serial
# from threading import Thread
# import threading
# import time

# class Lights():
#     def __init__(self, prt):
#         self.serial_port = Serial(port = prt, baudrate = 9600, timeout = 2)
#         self.enable = False
#         self.on = False
#         self.color = 0
#         self.flash = False
#         self.flash_state = False
#         self.cmask = 4294967295
    
#     def set_enable(self, state):
#         self.enable = state
        
#     def set_on(self, state):
#         self.on = state

#     def set_color(self, color):
#         self.color = color
    
#     def set_flash(self, flash):
#         self.flash = flash

#     def toggle_flash_state(self):
#         self.flash_state = not self.flash_state
    
#     def write_to_light(self):
#         if(self.on == True):
#             if(self.flash == True):
#                 if(self.flash_state == True):
#                     cvalue = self.color & self.cmask

#                 else:
#                     cvalue = 0
#                 print("flash toggle state: ", self.flash_state)
#                 self.toggle_flash_state()

#             else:
#                 cvalue = self.color & self.cmask
#         else:
#             cvalue = 0
        
#         print("cvalue: ", cvalue, " color: ", self.color)

#         self.serial_port.write(str(cvalue).encode())


# def loop(light):
#     while(light.enable == True):
#         print("writing to light") 
#         light.write_to_light()
#         # event.wait(1)
#         time.sleep(1)
#     light.set_on(False)
#     light.write_to_light()
from serial import Serial
import threading
from threading import Thread
import serial
import math
import time 

class Lights():   
    def __init__(self, prt, num_pixels):
        self.num_pixels = num_pixels
        self.BYTESPERPIXEL = 8
        self.baudRate = 3001000
        self.commPort = prt
        self.pixelCount = 2
        self.serial_port = Serial(port = self.commPort, baudrate = self.baudRate, bytesize = serial.SEVENBITS, stopbits = serial.STOPBITS_ONE, timeout = 2)

        self.orange = [0x5b,0x12,0x12,0x12,0x12,0x5b,0x5b,0x5b]
        self.off = [0x5b,0x5b,0x5b,0x5b,0x5b,0x5b,0x5b,0x5b]
        self.red = [0x5b,0x5b,0x12,0x12,0x12,0x5b,0x5b,0x5b]
        self.blue = [0x5b, 0x5b, 0x5b, 0x5b, 0x5b, 0x12, 0x12, 0x12]
        self.colorbuffer = [None]*16 #self.pixelCount

        self.enable = False
        self.on = False
        self.color = 0
        self.flash = False
        self.flash_state = False
        self.uartBuffer = self.off
      

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
    
    def compose_colors(self, color):
        outbuf = None
        if(color is 'RED'):
            out_buf = self.red
            for i in range(self.num_pixels):
                out_buf = out_buf + self.red
        
        if(color is 'ORANGE'):
            out_buf = self.orange
            for i in range(self.num_pixels):
                out_buf = out_buf + self.orange
        
        if(color is 'BLUE'):
            out_buf = self.blue
            for i in range(self.num_pixels):
                out_buf = out_buf + self.blue
        
        if(color is 'OFF'):
            out_buf = self.off
            for i in range(self.num_pixels):
                out_buf = out_buf + self.off

        return out_buf
    def write_to_light(self):
        if(self.on == True):
            if(self.flash == True):
                if(self.flash_state == True):
                    cvalue = self.compose_colors(self.color)

                else:
                    print("Turning off")
                  
                    cvalue = self.compose_colors('OFF')
                print("flash toggle state: ", self.flash_state)
                self.toggle_flash_state()

            else:
                cvalue = self.compose_colors(self.color)
        else:
            cvalue = self.compose_colors('OFF')
        
        print("cvalue: ", cvalue, " color: ", self.color)

        self.serial_port.write(cvalue)

    def loop(light):
        while(light.enable == True):
            print("writing to light") 
            light.write_to_light()
            # event.wait(1)
            time.sleep(1)
        light.set_on(False)
        light.write_to_light()

    def main(self):
      self.loop()


def loop(light):
    while(light.enable == True):
        print("writing to light") 
        light.write_to_light()
        # event.wait(1)
        time.sleep(1)
    #light.self_color()
    light.set_on(False)
    light.write_to_light()
# ntu = NeopixelToUART(prt='COM6', num_pixels=16)
# ntu.set_color('BLUE')
# ntu.set_on(True)
# ntu.set_flash(True)
# ntu.set_enable(True)
# ntu.main()



