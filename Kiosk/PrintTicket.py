# PrintTicket.py: Library with a class and methods to print
# bus tickets/passes for the Kiosk 

from Adafruit_Thermal import *
import time
from datetime import datetime, timedelta 
from PIL import Image
import os

class Ticket():

    # ticket_types = [0: 'Single'; 1: 'Day'; 2: 'Week'; 3: 'Month'; 4: 'Year']
    ticketFares = {'Single': 2.75, 'Day': 7.00, 'Week': 25.00, 'Month': 97.50, 'Year': 1072.50}
    # image_file = 'qr.png'
    
    def __init__(self, prt='COM5'):  #, ticketType='Single', img='qr.png'):
        self.serial_port = prt #Serial(port = prt, baudrate = 19200, timeout = 5)
        self.type = 'Single' # ticketType
        self.datetime = datetime.now()
        self.date = self.datetime.strftime("%b-%d-%Y")
        self.time = self.datetime.strftime("%H:%M:%S")
        self.expdate = self.date
        self.exptime = "23:59:59"
        self.qrcode = Image.open('qr.png')



    def set_type(self, ticketType):
        self.type = ticketType

    def set_datetime(self): 
        self.datetime = datetime.now()
        self.date = self.datetime.strftime("%b-%d-%Y")
        self.time = self.datetime.strftime("%H:%M:%S")
        # Set expiry time according to type
        if (self.type == 'Single'):
            self.expdate = self.date
        
        if (self.type == 'Day'):
            self.expdate = self.date

        if (self.type == 'Week'):
            self.expdate = (self.datetime + timedelta(days=6)).strftime("%b-%d-%Y")

        if (self.type == 'Month'):
            self.expdate = (self.datetime + timedelta(days=30)).strftime("%b-%d-%Y")

        if (self.type == 'Year'):
            self.expdate = (self.datetime + timedelta(days=364)).strftime("%b-%d-%Y")
            self.exptime = "23:59:59"


    def set_qrcode(self, img):
        self.qrcode = img


    def printTicket(self, ticketType, img=None):
        
        self.set_type(ticketType)
        self.set_datetime()
        if img != None:
            self.set_qrcode(img)

        # Bus Ticket 
        printer = Adafruit_Thermal(self.serial_port, 19200, timeout=5)
        printer.flush()
        printer.justify('C')    # Center justified
        printer.setSize('M')    # Medium size
        printer.boldOn()
        printer.println("Welcome to OnwardPGH Kiosk!")
        printer.boldOff()

        printer.justify('L')    # Left justified
        printer.setSize('S')    # Small size
        printer.print("\nDate: ")
        printer.justify('R')    # Right justified
        printer.print(self.date)

        printer.justify('L')    # Left justified
        printer.print("\nTime: ")
        printer.justify('R')    # Right justified
        printer.print(self.time)

        printer.justify('L')    # Left justified
        printer.print("\nTicket Type: ")
        printer.justify('R')    # Right justified
        printer.print(self.type, " Pass")

        printer.justify('L')    # Left justified
        printer.print("\nExpiry: ")
        printer.justify('R')    # Right justified
        printer.print(self.expdate, "  ", self.exptime)

        printer.justify('L')    # Left justified
        printer.boldOn()        # Bold on
        printer.print("\n\nFare: ")
        # printer.justify('R')    # Right justified
        # printer.setSize('M')
        printer.print("${:.2f}".format(self.ticketFares[self.type]))
        printer.boldOff()       # Bold off

        printer.println("\n")
        
        # printer.justify('L')    # Left justified

        printer.justify('C')    # Center justified
        printer.printImage(self.qrcode)

        printer.println("\n")
        
        printer.justify('C')    # Center justified
        printer.println("Thank you for using OnwardPGH!")
        printer.println("Submit a text or audio feedback at the Kiosk for a chance to win a free bus ticket!")

        printer.feed(2)

        printer.sleep()      # Tell printer to sleep
        printer.wake()       # Call wake() before printing again, even if reset
        printer.setDefault() # Restore printer to defaults


if __name__ == '__main__':
    ticket = Ticket(prt='COM5')
    ticket.printTicket(ticketType='Single')
