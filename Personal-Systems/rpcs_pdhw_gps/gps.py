from time import sleep
import serial
from threading import Thread, Lock

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

def decode(coord):
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

def parseGPS(data):
    global _gps_valid
    global _latitude
    global _longitude
    #print(data, end='') #prints raw data
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            _mutex.acquire()
            _gps_valid = 0
            _mutex.release()
            #print("\nNo satellite data available.\n")
            return
        #print("-----Parsing GPRMC-----")
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

        _mutex.acquire()
        _gps_valid = 1
        _latitude = int(latitude[0]) + (float(latitude[2])/60)
        if dirLat == 'S':
            _latitude = -_latitude
        _longitude = int(longitute[0]) + (float(longitute[2])/60)
        if dirLon == 'W':
            _longitude = -_longitude
        _mutex.release()


        #print("\nLatitude: " + str(int(latitude[0]) + (float(latitude[2])/60)) + dirLat) 
        #print("Longitute: " + str(int(longitute[0]) + (float(longitute[2])/60)) + dirLon)
        #print("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s,True Course : %s, Date : %s, Magnetic Variation : %s(%s),Checksum : %s "%   (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum))
        

_gps_valid = 0
_date_y = 0
_date_m = 0
_date_d = 0
_time_h = 0
_time_m = 0
_time_s = 0
_latitude =0
_dir_latitude = 0
_longitude = 0
_dir_longitude = 0
_speed = 0
_true_course = 0
_variation = 0
_degree = 0
_checksum = 0



def _fetchGPS():
    print("Receiving GPS data\n")
    ser = serial.Serial(port, baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)
    while True:
        data = ser.readline().decode('utf-8')
        parseGPS(data)

_mutex = Lock()

def initGPS():
    print("Connecting Port..")
    try:
        serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
        serw.write('AT+QGPS=1\r'.encode())
        serw.close()
        sleep(1)
    except Exception as e: 
        print("Serial port connection failed.")
        print(e)
    t = Thread(target = _fetchGPS)
    t.start()

def getGPS():
    global _gps_valid
    _mutex.acquire()
    gps_valid = _gps_valid
    latitude = _latitude
    longitude = _longitude
    _mutex.release()
    return gps_valid, latitude, longitude
