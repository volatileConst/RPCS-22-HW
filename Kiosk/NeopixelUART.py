
from serial import Serial
<<<<<<< HEAD
import serial
=======
>>>>>>> c63586cd19fc23ccd503b5017bfd4675eac33a5a
import math
import time 

class NeopixelToUART():
<<<<<<< HEAD
    
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
        for i in range(15):
            self.uartBuffer = self.uartBuffer + self.off
        self.sinColorTable = [None]*128
      

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
            cvalue = self.compose_colors(self.color)
        
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



ntu = NeopixelToUART(prt='COM5', num_pixels=16)
ntu.set_color('BLUE')
ntu.set_on(True)
ntu.set_flash(True)
ntu.set_enable(True)
=======

    def __init__(self, prt):
        self.BYTESPERPIXEL = 8
        self.baudRate = 3000800
        self.commPort = prt
        self.pixelCount = 16
        self.serial_port = Serial(port = self.commPort, baudrate = self.baudRate, timeout = 2)

        self.bitTriplets = [0x5b, 0x1b, 0x53, 0x13, 0x5a, 0x1a, 0x52, 0x12]

        self.colorbuffer = [None]*16 #self.pixelCount
        self.uartBuffer = [None]*(self.pixelCount*self.BYTESPERPIXEL)
        self.sinColorTable = [None]*128
        self.fillColorTable()

    def translateColors(self):
    
        for i in range(self.pixelCount):
            
            # print("color i ", i, " ", self.colorbuffer[i])
            # if i == 6:
            color = self.colorbuffer[i]
            # else:
            #     color = 0

            pixOffset = i * self.BYTESPERPIXEL
            
            # only 8 permutations so no need to use a for loop
            self.uartBuffer[pixOffset] = self.bitTriplets[(color >> 21) & 0x07]
            self.uartBuffer[pixOffset + 1] = self.bitTriplets[(color >> 18) & 0x07]
            self.uartBuffer[pixOffset + 2] = self.bitTriplets[(color >> 15) & 0x07]
            self.uartBuffer[pixOffset + 3] = self.bitTriplets[(color >> 12) & 0x07]
            self.uartBuffer[pixOffset + 4] = self.bitTriplets[(color >> 9) & 0x07]
            self.uartBuffer[pixOffset + 5] = self.bitTriplets[(color >> 6) & 0x07]
            self.uartBuffer[pixOffset + 6] = self.bitTriplets[(color >> 3) & 0x07]
            self.uartBuffer[pixOffset + 7] = self.bitTriplets[color & 0x07]
    

    def fillColorTable(self):
        refValues = [None]*len(self.sinColorTable)
        phase = 120
        # onTimeRatio = len(refValues) * 180 / (phase * 3)
        onTimeRatio = 128 * 180 / (phase * 3)
        radian = math.pi/onTimeRatio

        for i in range(len(refValues)):
            if (i < onTimeRatio):
                refValues[i] = int(math.sin(radian * i) * 255)
            else:
                refValues[i] = 0

        for i in range(len(self.sinColorTable)):
            greenOffset = int((i + (onTimeRatio * phase * 2 / 180)) % len(self.sinColorTable))
            blueOffset = int((i + (onTimeRatio * phase / 180)) % len(self.sinColorTable))

            self.sinColorTable[i] = (refValues[i] << 8) | (refValues[greenOffset] << 16) | (refValues[blueOffset])
    
    def setPixels(self, color):

        print("color ", color)
        for i in range(16):
            self.colorbuffer[i] = color
            print("color buffer i", i, " ", self.colorbuffer[i])


    def main(self):
        print("Bytes to send: ", len(self.uartBuffer))
        # color=0x000000
        color=0x0000FF  # Blue
        # color = self.sinColorTable[127]
        print("color ", color)
        self.setPixels(color)
        self.translateColors()
        self.serial_port.write(self.uartBuffer)
        self.serial_port.flush()
        time.sleep(5)
        color=0x00FF00  # Red
        print("color ", color)
        self.setPixels(color)
        self.translateColors()
        self.serial_port.write(self.uartBuffer)
        self.serial_port.flush()
        time.sleep(5)
        color=0xFF0000  # Green
        print("color ", color)
        self.setPixels(color)
        self.translateColors()
        self.serial_port.write(self.uartBuffer)
        self.serial_port.flush()



ntu = NeopixelToUART(prt='COM5')
>>>>>>> c63586cd19fc23ccd503b5017bfd4675eac33a5a
ntu.main()

