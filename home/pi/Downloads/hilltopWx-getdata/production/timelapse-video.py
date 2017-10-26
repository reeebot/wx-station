
#run shell command
#make timelapse video for the hour
from subprocess import call
call(["ffmpeg -y -f image2 -i /var/www/html/camerapics/timelapse/*.jpg -r 24 -vcodec libx264 -profile high -preset slow /var/www/html/camerapics/videos/timelapse.mp4"])

# delete image files
	os.remove()