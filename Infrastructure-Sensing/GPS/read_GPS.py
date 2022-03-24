# initializes GPS and fetches latitude/longitude

from time import sleep
import serial

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"
serial_port = 0

def connect_port():
    global serial_port

    # initializes port connection
    print("Connecting Port..")
    try:
        serw = serial.Serial(portwrite, baudrate=115200, timeout=1, rtscts=True, dsrdtr=True)
        serw.write('AT+QGPS=1\r'.encode())
        serw.close()
        sleep(1)
    except Exception as e: 
        print("Serial port connection failed.")
        print(e)

    print("Receiving GPS data\n")
    serial_port = serial.Serial(port, baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)

def decode(coord):
    # converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

def sample_GPS():
    # returns tuple of latitude/longitude
    latitude = 0
    longitude = 0

    # keep reading GPS data till we get the latitude/longitude
    data = "GPS_log"
    while data[0:6] != "$GPRMC":
        data = serial_port.readline().decode('utf-8')

    sdata = data.split(",")
    if sdata[2] == 'V':
        print("\nNo satellite data available.\n")
        return (latitude, longitude)
    print("-----Parsing GPRMC-----")
    time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
    lat = decode(sdata[3]) #latitude
    dirLat = sdata[4]      #latitude direction N/S
    lon = decode(sdata[5]) #longitute
    dirLon = sdata[6]      #longitude direction E/W
    speed = sdata[7]       #Speed in knots
    trCourse = sdata[8]    #True course
    date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #date
    variation = sdata[10]  #variation
    degreeChecksum = sdata[13] #Checksum
    dc = degreeChecksum.split("*")
    degree = dc[0]        #degree
    checksum = dc[1]      #checksum

    latitude = lat.split() # parsing latitude
    longitute = lon.split() # parsing longitute

    print("\nLatitude: " + str(int(latitude[0]) + (float(latitude[2])/60)) + dirLat) 
    print("Longitute: " + str(int(longitute[0]) + (float(longitute[2])/60)) + dirLon)

    coordinates = (latitude, longitude)
    return coordinates

def initialize_GPS():
    # connect to serial port
    connect_port()

    # sample data for ~10 seconds to initialize GPS
    initialization_count = 0
    while initialization_count < 10:
        sample_GPS()
        sleep(1)
        initialization_count += 1