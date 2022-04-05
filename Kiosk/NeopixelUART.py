
from serial import Serial
import math
import time 

class NeopixelToUART():

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
ntu.main()

