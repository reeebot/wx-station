import picamera
from time import sleep

camera = picamera.PiCamera()

camera.start_preview()

#camera.start_recording('video.h264')
sleep(10)
#camera.stop_recording()



camera.stop_preview()
