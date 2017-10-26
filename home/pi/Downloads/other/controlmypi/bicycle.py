'''
Created on 6 Nov 2012

Bicycle telemetry recorder with Live web dashboard through ControlMyPi.com

See: http://jeremyblythe.blogspot.com
     http://www.controlmypi.com
     Follow me on Twitter for updates: @jerbly
     
@author: Jeremy Blythe
'''

import serial
import subprocess
import mcp3008
import time
from controlmypi import ControlMyPi

JABBER_ID = 'you@your.jabber.host'
JABBER_PASSWORD = 'yourpassword'
SHORT_ID = 'bicycle'
FRIENDLY_NAME = 'Bicycle telemetry system'
PANEL_FORM = [
             [ ['S','locked',''] ],
             [ ['O'] ],
             [ ['P','streetview',''],['P','map',''] ],
             [ ['C'] ],
             [ ['O'] ],
             [ ['L','Speed'],['G','speed','mph',0,0,50], ['L','Height'],['S','height',''] ],
             [ ['C'] ],
             [ ['L','Accelerations'] ],
             [ ['G','accx','X',0,-3,3], ['G','accy','Y',0,-3,3], ['G','accz','Z',1,-3,3] ],
             [ ['L','Trace file'],['B','start_button','Start'],['B','stop_button','Stop'],['S','recording_state','-'] ]
             ]

API_KEY = '&key=YOUR_API_KEY'
STREET_VIEW_URL = 'http://maps.googleapis.com/maps/api/streetview?size=360x300&location=%s,%s&fov=60&heading=%s&pitch=0&sensor=true'+API_KEY
MAP_URL = 'http://maps.googleapis.com/maps/api/staticmap?center=%s,%s&zoom=15&size=360x300&sensor=true&markers=%s,%s'+API_KEY

class GPS:
    def __init__(self):
        self.height = '0'
        self.time_stamp = ''
        self.active = False
        self.lat = None
        self.lat_dir = None
        self.lon = None
        self.lon_dir = None
        self.speed = None
        self.heading = None
        self.date = ''
        # Connect to GPS at default 9600 baud
        self.ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.01)
        # Switch GPS to faster baud
        self.send_and_get_ack('251',',38400')
        # Assume success - close and re-open serial port at new speed
        self.ser.close()
        self.ser = serial.Serial('/dev/ttyAMA0',38400,timeout=0.01)
        # Set GPS into RMC and GGA only mode
        self.send_and_get_ack('314',',0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Set GPS into 10Hz mode
        self.send_and_get_ack('220',',100')

    def checksum(self,cmd):
        calc_cksum = 0
        for s in cmd:
            calc_cksum ^= ord(s)
        return '$'+cmd+'*'+hex(calc_cksum)[2:]

    def send_and_get_ack(self,cmdno,cmdstr):
        '''Send the cmd and wait for the ack'''
        #$PMTK001,604,3*32
        #PMTK001,Cmd,Flag 
        #Cmd: The command / packet type the acknowledge responds. 
        #Flag: .0. = Invalid command / packet. 
        #.1. = Unsupported command / packet type 
        #.2. = Valid command / packet, but action failed 
        #.3. = Valid command / packet, and action succeeded 
        cmd = 'PMTK%s%s' % (cmdno,cmdstr)
        msg = self.checksum(cmd)+chr(13)+chr(10)
        #print '>>>%s' % cmd
        self.ser.write(msg)
        ack = False
        timeout = 300
        while (not ack) and timeout > 0:
            line = str(self.ser.readline())
            if line.startswith('$PMTK001'):
                tokens = line.split(',')
                ack = tokens[2][0] == '3'
                #print '<<<%s success=%s' % (line,ack)
            timeout -= 1
        return ack

    def read(self):
        '''Read the GPS'''
        line = str(self.ser.readline())
        #print line
    
        if line.startswith('$GPGGA'):
            # $GPGGA,210612.300,5128.5791,N,00058.5165,W,1,8,1.18,41.9,M,47.3,M,,*79
            # 9 = Height in metres
            tokens = line.split(',')
            if len(tokens) < 15:
                return
            try:
                self.height = tokens[9]
            except ValueError as e:
                print e    
        elif line.startswith('$GPRMC'):
            # $GPRMC,105215.000,A,5128.5775,N,00058.5070,W,0.12,103.43,211012,,,A*78
            # 1 = Time
            # 2 = (A)ctive or (V)oid
            # 3 = Latitude
            # 5 = Longitude
            # 7 = Speed in knots
            # 8 = Compass heading
            # 9 = Date
            #Divide minutes by 60 and add to degrees. West and South = negative
            #Multiply knots my 1.15078 to get mph.
            tokens = line.split(',')
            if len(tokens) < 10:
                return
            try:
                self.time_stamp = tokens[1]
                self.active = tokens[2] == 'A'
                self.lat = tokens[3]
                self.lat_dir = tokens[4]
                self.lon = tokens[5]
                self.lon_dir = tokens[6]
                self.speed = tokens[7]
                self.heading = tokens[8]
                self.date = tokens[9]
                if self.active:
                    self.lat = float(self.lat[:2]) + float(self.lat[2:])/60.0
                    if self.lat_dir == 'S':
                        self.lat = -self.lat
                    self.lon = float(self.lon[:3]) + float(self.lon[3:])/60.0
                    if self.lon_dir == 'W':
                        self.lon = -self.lon
                    self.speed = float(self.speed) * 1.15078
            except ValueError as e:
                print e
        
class TextStar:
    def __init__(self, on_rec_button):
        self.LCD_UPDATE_DELAY = 5
        self.lcd_update = 0
        self.page = 0
        self.ser = serial.Serial('/dev/ttyUSB0',115200,timeout=0.01)
        # Throw away first few key presses after waiting for the screen to start up
        time.sleep(3)
        self.ser.read(16)
        self.on_rec_button = on_rec_button
    
    def get_addr(self,interface):
        try:
            s = subprocess.check_output(["ip","addr","show",interface])
            return s.split('\n')[2].strip().split(' ')[1].split('/')[0]
        except:
            return '?.?.?.?'
    
    def write_ip_addresses(self):
        self.ser.write(chr(254)+'P'+chr(1)+chr(1))
        self.ser.write('e'+self.get_addr('eth0').rjust(15)+'p'+self.get_addr('ppp0').rjust(15))

    def update(self,gps,acc,rec):
        self.lcd_update += 1
        if self.lcd_update > self.LCD_UPDATE_DELAY:
            self.lcd_update = 0
            self.ser.write(chr(254)+'P'+chr(1)+chr(1))
            
            if not gps.active and (self.page == 0 or self.page == 1):
                self.ser.write('NO FIX: '+gps.date+' '+rec.recording)
                self.ser.write(gps.time_stamp.ljust(16))
            elif self.page == 0:
                self.ser.write(('%.8f' % gps.lat).rjust(14)+" "+rec.recording)
                self.ser.write(('%.8f' % gps.lon).rjust(14)+"  ")
            elif self.page == 1:
                #0.069 223.03 48.9 -0.010 0.010 0.980
                self.ser.write('{: .3f}{:>9} '.format(gps.speed,gps.height))
                if acc:
                    self.ser.write('{: .2f}{: .2f}{: .2f}'.format(*acc))
                else:
                    self.ser.write(' '*16)

    def read_key(self):
        key = str(self.ser.read(1))
        if key != '' and key in 'abcd':
            self.lcd_update = self.LCD_UPDATE_DELAY
            if key == 'c':
                self.on_rec_button()
            elif key == 'a':
                self.page += 1
                if self.page > 2:
                    self.page = 0
                elif self.page == 2:
                    self.write_ip_addresses()
        
class Recorder:
    def __init__(self,gps,cmp):
        self.gps = gps
        self.cmp = cmp
        self.recording = 's'
        self.rec_file = None

    def start(self):
        if self.recording == 's':
            self.recording = 'r'
            self.rec_file = open("/home/pi/gps-"+self.gps.date+self.gps.time_stamp+".log", "a")
            self.cmp.update_status( {'recording_state':'Recording'} )
    
    def stop(self):
        if self.recording == 'r':
            self.recording = 's'
            self.rec_file.close()
            self.cmp.update_status( {'recording_state':'Stopped - [%s]' % self.rec_file.name} )

    def update(self,acc):
        if self.recording == 'r':
            if acc:
                acc_str = '%.2f %.2f %.2f' % acc
            else:
                acc_str = '- - -'
                
            if self.gps.active:
                self.rec_file.write('%s %s %.8f %.8f %.3f %s %s %s\n' % (self.gps.date, self.gps.time_stamp, self.gps.lat, self.gps.lon, self.gps.speed, self.gps.heading, self.gps.height, acc_str))
            else:
                self.rec_file.write('%s %s - - - - - %s\n' % (self.gps.date, self.gps.time_stamp, acc_str))

class Accelerometer:
    def read_accelerometer(self):
        '''Read the 3 axis accelerometer using the MCP3008. 
           Each axis is tuned to show +1g when oriented towards the ground, this will be different
           for everyone and dependent on physical factors - mostly how flat it's mounted.
           The result is rounded to 2 decimal places as there is too much noise to be more
           accurate than this.
           Returns a tuple (X,Y,Z).'''  
        x = mcp3008.readadc(0)
        y = mcp3008.readadc(1)
        z = mcp3008.readadc(2)
        return ( round((x-504)/102.0,2) , round((y-507)/105.0,2) , round((z-515)/102.0,2) )

    
# Start the GPS
gps = GPS()

# Create the Accelerometer object. Change to acc=None if you don't have an accelerometer.
acc = Accelerometer()

# Control My Pi
def on_control_message(conn, key, value):
    if key == 'start_button':    
        rec.start()
    elif key == 'stop_button':
        rec.stop()

conn = ControlMyPi(JABBER_ID, JABBER_PASSWORD, SHORT_ID, FRIENDLY_NAME, PANEL_FORM, on_control_message)

# Recording
rec = Recorder(gps, conn)

def on_rec_button():
    if rec.recording == 's':
        rec.start()
    else:
        rec.stop()    

# Start the TextStar LCD. Change to lcd=None if you don't have a TextStar LCD.
lcd = TextStar(on_rec_button)
        
if conn.start_control():
    try:
        conn.update_status( {'recording_state':'Stopped'} )
        # Start main loop
        old_time_stamp = 'old'
        CMP_UPDATE_DELAY = 50
        cmp_update = 0
        
        while True:
            #Read the 3 axis accelerometer
            if acc:
                xyz = acc.read_accelerometer()
            else:
                xyz = None
                
            #Read GPS
            gps.read()
                    
            #Update ControlMyPi, LCD and Recorder if we have a new reading 
            if gps.time_stamp != old_time_stamp:
                if lcd:
                    lcd.update(gps, xyz, rec)      

                # Don't update ControlMyPi every tick, it'll be too much - approx. 5 seconds is
                # about right as it gives the browser time to fetch the streetview and map 
                cmp_update += 1
                if cmp_update > CMP_UPDATE_DELAY:
                    cmp_update = 0
                    status = {}
                    if xyz:
                        status['accx'] = xyz[0]
                        status['accy'] = xyz[1]
                        status['accz'] = xyz[2]
                    
                    if gps.active:
                        status['locked'] = 'GPS locked'
                        slat = str(gps.lat)
                        slon = str(gps.lon)
                        status['streetview'] = STREET_VIEW_URL % (slat,slon,gps.heading)
                        status['map'] = MAP_URL % (slat,slon,slat,slon)
                        status['speed'] = int(round(gps.speed))
                        status['height'] = '{:>9}'.format(gps.height)
                        conn.update_status(status)
                    else:
                        status['locked'] = 'GPS NOT LOCKED'
                        conn.update_status(status)
              
                #Update recorder every tick
                rec.update(xyz)
        
                old_time_stamp = gps.time_stamp
        
            #Read keypad
            if lcd:        
                lcd.read_key()
    finally:
        conn.stop_control()
else:
    print("FAILED TO CONNECT")
