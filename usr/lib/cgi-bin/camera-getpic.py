import time
import picamera
with picamera.PiCamera() as camera:

	camera.start_preview()
	camera.resolution = (1024, 768)
	#camera.vflip = True
	#camera.hflip = True
	time.sleep(2)

	camera.capture('/var/www/html/camerapics/live.jpg')
#	camera.capture('/var/www/html/camerapics/timelapse/%s.jpg'%time.strftime("%Y%m%d-%H%M%S"))

	camera.stop_preview()