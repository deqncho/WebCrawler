import pdfkit
import time

start_time = time.time()
pdfkit.from_url('http://www.inf.ed.ac.uk/teaching/courses/pi/2015_2016/index.html', 'out.pdf')

seconds_elapsed = int(time.time() - start_time)
formatted_seconds = seconds_elapsed % 60
minutes_elapsed = int(seconds_elapsed / 60)
formatted_minutes = minutes_elapsed % 60
hours_elapsed = int(minutes_elapsed / 60)
print "Time elapsed: {0} hours: {1} minutes: {2} seconds".format(hours_elapsed, formatted_minutes, formatted_seconds)