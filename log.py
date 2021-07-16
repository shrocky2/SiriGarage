import os
import RPi.GPIO as GPIO
import time
from datetime import datetime


from config import (NUMBER_OF_DOORS, SENSORS_PER_DOOR)

logfile = open("static/log.txt","a")
logfile.write(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))
logfile.close()
print(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))

print(" Control + C to exit Program")
print(" Number of Doors: " + str(NUMBER_OF_DOORS))
print(" Number of Sensors Per Door: " + str(SENSORS_PER_DOOR))


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # Door 1 is Closed sensor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # Door 1 is Open sensor
GPIO.setup(29, GPIO.IN, GPIO.PUD_UP) # Door 2 is Closed sensor
GPIO.setup(31, GPIO.IN, GPIO.PUD_UP) # Door 2 is Open sensor
GPIO.setup(33, GPIO.IN, GPIO.PUD_UP) # Door 3 is Closed sensor
GPIO.setup(37, GPIO.IN, GPIO.PUD_UP) # Door 3 is Open sensor
time.sleep(1)

TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')  #Default Time
Door1_OpenTimer = 0  		#Default start status turns timer off
Door1_OpenTimerMessageSent = 1 	#Turn off messages until timer is started
Door2_OpenTimer = 0  		#Default start status turns timer off
Door2_OpenTimerMessageSent = 1  #Turn off messages until timer is started
Door3_OpenTimer = 0  		#Default start status turns timer off
Door3_OpenTimerMessageSent = 1  #Turn off messages until timer is started

TimeDoor1_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
TimeDoor2_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
TimeDoor3_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

try:
	while 1 >= 0:
		time.sleep(1)
		if Door1_OpenTimer != 0:  #Door Open Timer has Started
			currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
			if (currentTimeDate - TimeDoor1_Opened).seconds > 900 and Door1_OpenTimerMessageSent == 0:
				print("Your Garage Door #1 has been Open for 15 minutes")	
				Door1_OpenTimerMessageSent = 1
		if Door2_OpenTimer != 0:  #Door Open Timer has Started
			currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
			if (currentTimeDate - TimeDoor2_Opened).seconds > 900 and Door2_OpenTimerMessageSent == 0:
				print("Your Garage Door #2 has been Open for 15 minutes")
				Door2_OpenTimerMessageSent = 1
		if Door3_OpenTimer != 0:  #Door Open Timer has Started
			currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
			if (currentTimeDate - TimeDoor3_Opened).seconds > 900 and Door3_OpenTimerMessageSent == 0:
				print("Your Garage Door #3 has been Open for 15 minutes")
				Door3_OpenTimerMessageSent = 1

#------------------------------- Door 1 Code -------------------------------

		if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:  #Door Status is Unknown (or Open if 1 Sensor Per Door)
			logfile = open("static/log.txt","a")
			if SENSORS_PER_DOOR == 1:
				logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Open \n"))
				print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Open"))
			else:
				logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Opening/Closing \n"))
				print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Opening/Closing"))
			logfile.close()
		else:		
			while GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
				time.sleep(.5)
			else:
				if GPIO.input(16) == GPIO.LOW:  #Door is Closed
					logfile = open("static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Closed \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Closed"))
					Door1_OpenTimer = 0

				if GPIO.input(18) == GPIO.LOW:  #Door is Open
					logfile = open("static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Open \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #1 Open"))
					#Start Door Open Timer
					TimeDoor1_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
					Door1_OpenTimer = 1
					Door1_OpenTimerMessageSent = 0

#------------------------------- Door 2 Code -------------------------------

		if NUMBER_OF_DOORS > 1:
			if GPIO.input(29) == GPIO.HIGH and GPIO.input(31) == GPIO.HIGH:  #Door Status is Unknown (or Open if 1 Sensor Per Door)
				if Door2_OpenTimer == 0:
					logfile = open("static/log.txt","a")
				if SENSORS_PER_DOOR == 1:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open"))
				else:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Opening/Closing \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Opening/Closing"))
				logfile.close()
				Door2_OpenTimer = 1
			else:
				while GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
					time.sleep(.5)
				else:
					if GPIO.input(29) == GPIO.LOW:  #Door is Closed
						logfile = open("static/log.txt","a")
						logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Closed \n"))
						logfile.close()
						print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Closed"))
						Door2_OpenTimer = 0

				if GPIO.input(31) == GPIO.LOW:  #Door is Open
					logfile = open("static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #2 Open"))
					#Start Door Open Timer
					TimeDoor2_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
					Door2_OpenTimer = 2
					Door2_OpenTimerMessageSent = 0

#------------------------------- Door 3 Code -------------------------------

		if NUMBER_OF_DOORS > 2:
			if GPIO.input(33) == GPIO.HIGH and GPIO.input(37) == GPIO.HIGH:  #Door Status is Unknown (or Open if 1 Sensor Per Door)
				if Door3_OpenTimer == 0:
					logfile = open("static/log.txt","a")
				if SENSORS_PER_DOOR == 1:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open"))
				else:
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Opening/Closing \n"))
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Opening/Closing"))
				logfile.close()
				Door3_OpenTimer = 1
			else:
				while GPIO.input(33) == GPIO.HIGH and GPIO.input(37) == GPIO.HIGH:
					time.sleep(.5)
				else:
					if GPIO.input(33) == GPIO.LOW:  #Door is Closed
						logfile = open("static/log.txt","a")
						logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Closed \n"))
						logfile.close()
						print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Closed"))
						Door3_OpenTimer = 0

				if GPIO.input(37) == GPIO.LOW:  #Door is Open
					logfile = open("static/log.txt","a")
					logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open \n"))
					logfile.close()
					print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door #3 Open"))
					#Start Door Open Timer
					TimeDoor2_Opened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
					Door3_OpenTimer = 2
					Door3_OpenTimerMessageSent = 0



except KeyboardInterrupt:
	logfile = open("static/log.txt","a")
	logfile.write(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
	logfile.close()
	print(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
	GPIO.cleanup()
