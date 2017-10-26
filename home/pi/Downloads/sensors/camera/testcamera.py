
import time

import picamera

with picamera.PiCamera() as camera:
    
    camera.start_preview()
    
    time.sleep(0)
    
    camera.capture('/home/pi/Desktop/rebot/')
    
    camera.stop_preview()