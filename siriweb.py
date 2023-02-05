import os
import time
from datetime import datetime
from flask import Flask, render_template, request
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(socket.gethostname() + ".local")

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # Door 1 is Closed sensor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # Door 1 is Open sensor
GPIO.setup(29, GPIO.IN, GPIO.PUD_UP) # Door 2 is Closed sensor
GPIO.setup(31, GPIO.IN, GPIO.PUD_UP) # Door 2 is Open sensor
GPIO.setup(33, GPIO.IN, GPIO.PUD_UP) # Door 3 is Closed sensor
GPIO.setup(37, GPIO.IN, GPIO.PUD_UP) # Door 3 is Open sensor

GPIO.setup(7, GPIO.OUT)			#Door 1 Relay to Open Door
GPIO.output(7, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)		#Door 2 Relay to Open Door
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)		#Door 3 Relay to Open Door
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)		#Not Used for the project
GPIO.output(15, GPIO.HIGH)

from config import (
	PORT,
	ENABLE_PASSWORD,
	PASSWORD,
	ENABLE_SIRI,
	SIRI_PASSWORD,
	BG_COLOR_QUESTION,
	BG_COLOR_OPEN,
	BG_COLOR_CLOSED,
	IMAGE_QUESTION,
	IMAGE_OPEN,
	IMAGE_CLOSED,
	NUMBER_OF_DOORS,
	DOOR_1_NAME,
	DOOR_2_NAME,
	DOOR_3_NAME,
	SENSORS_PER_DOOR,
	ADMIN,
	ADMIN_PASS,
)

directory = os.getcwd()
APP_PATH = os.path.abspath(__file__)
LOG_FILE = directory + '/log.py'

global No_Refresh
No_Refresh = int(datetime.now().strftime("%d%m"))
Refresher = int(datetime.now().strftime("%d%m"))
BadPassword = 0

Any_Door_Open = 1			#Default Status, If any door is Not Closed, this will be greater than 0
bgcolor = BG_COLOR_QUESTION		#Default Status, Door is questionable, so background yellow
door1image = IMAGE_QUESTION		#Default Status, Door is questionable, so image is question mark
door2image = IMAGE_QUESTION		#Default Status, Door is questionable, so image is question mark
door3image = IMAGE_QUESTION		#Default Status, Door is questionable, so image is question mark

if NUMBER_OF_DOORS == 1:
	door1 = "inline-block"
	door2 = "none"
	door3 = "none"
	imagesize = 100
elif NUMBER_OF_DOORS == 2:
	door1 = "inline-block"
	door2 = "inline-block"
	door3 = "none"
	imagesize = 100
elif NUMBER_OF_DOORS == 3:
	door1 = "inline-block"
	door2 = "inline-block"
	door3 = "inline-block"
	imagesize = 100

app = Flask(__name__)

print('-------------------------------------------')
print('\n Hostname of your Pi: ' + hostname)
print(' IP address of Pi: ' + ip_address)
print('')
print(' Garage Door Status Found at: http://' + ip_address + ':' + str(PORT))
print(' Settings Can Be Found at: http://' + ip_address + ':' + str(PORT) + '/Settings')
print(' Siri Setup Instructions Can Be Found at: http://' + ip_address + ':' + str(PORT) + '/page/sirisetup.html')
print('')
print('-------------------------------------------')



@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		global BadPassword
		global No_Refresh
		code = request.form['garagecode']
		Door_To_Open = request.form.get('garagedoorradio', "UNKNOWN")
		Password_Counter = int(request.form.get('No_Refresh', "0"))

		if code == PASSWORD and ENABLE_PASSWORD == "YES" and Password_Counter == No_Refresh and BadPassword <= 5:  # 12345678 is the Default Password that Opens Garage Door (Code if Password is Correct)
			print("Door requested to open: " + Door_To_Open)
			No_Refresh = No_Refresh + 1;

			if Door_To_Open == "door1":
				GPIO.output(7, GPIO.LOW)
				time.sleep(1)
				GPIO.output(7, GPIO.HIGH)
				time.sleep(2)
			if Door_To_Open == "door2":
				GPIO.output(11, GPIO.LOW)
				time.sleep(1)
				GPIO.output(11, GPIO.HIGH)
				time.sleep(2)
			if Door_To_Open == "door2":
				GPIO.output(13, GPIO.LOW)
				time.sleep(1)
				GPIO.output(13, GPIO.HIGH)
				time.sleep(2)
			
	
		else:  		# 12345678 is the Password that Opens Garage Door (Code if Password is Incorrect)
			if code == "":
				code = "NULL"
			else:
				BadPassword += 1
				logfile = open("static/log.txt","a")
				logfile.write("     " + datetime.now().strftime(request.environ['REMOTE_ADDR'] + "     Password Entered: " + code + " -- %Y/%m/%d -- %H:%M  \n"))
				logfile.close()
				print(request.environ['REMOTE_ADDR'] + " -- " + str(BadPassword) + " wrong password(s) have been entered!")

			if BadPassword > 5:
				logfile = open("static/log.txt","a")
				logfile.write("     " + datetime.now().strftime(request.environ['REMOTE_ADDR'] + "     Too Many Wrong Passwords, System Disabled.  -- %Y/%m/%d -- %H:%M  \n"))
				logfile.close()
				print("Garage Code Entered: " + code)


	door1image = IMAGE_QUESTION		#Default Status, Door is questionable, so image is question mark
	door2image = IMAGE_QUESTION		#Default Status, Door is questionable, so image is question mark
	door3image = IMAGE_QUESTION		#Default Status, Door is questionable, so image is question mark

	if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
		if SENSORS_PER_DOOR == 1:
			print("Door 1 is Open")
			door1image = IMAGE_OPEN
		else:
			print("Door 1 is Opening/Closing")
			door1image = IMAGE_QUESTION
		Any_Door_Open = 1
	else:
		if GPIO.input(16) == GPIO.LOW:
			print("Door 1 is Closed")
			door1image = IMAGE_CLOSED
			Any_Door_Open = 0
		if GPIO.input(18) == GPIO.LOW:
			print("Door 1 is Open")
			door1image = IMAGE_OPEN
			Any_Door_Open = 2

	if NUMBER_OF_DOORS > 1:
		if GPIO.input(29) == GPIO.HIGH and GPIO.input(31) == GPIO.HIGH:
			if SENSORS_PER_DOOR == 1:
				print("Door 2 is Open")
				door2image = IMAGE_OPEN
			else:
				print("Door 2 is Opening/Closing")
				door2image = IMAGE_QUESTION
			Any_Door_Open = Any_Door_Open + 1
		else:
			if GPIO.input(29) == GPIO.LOW:
				print("Door 2 is Closed")
				door2image = IMAGE_CLOSED
			if GPIO.input(31) == GPIO.LOW:
				print("Door 2 is Open")
				door2image = IMAGE_OPEN
				Any_Door_Open = Any_Door_Open + 2

	if NUMBER_OF_DOORS == 3:
		if GPIO.input(33) == GPIO.HIGH and GPIO.input(37) == GPIO.HIGH:
			if SENSORS_PER_DOOR == 1:
				print("Door 3 is Open")
				door3image = IMAGE_OPEN
			else:
				print("Door 3 is Opening/Closing")
				door3image = IMAGE_QUESTION
			Any_Door_Open = Any_Door_Open + 1
		else:
			if GPIO.input(33) == GPIO.LOW:
				print("Door 3 is Closed")
				door3image = IMAGE_CLOSED
			if GPIO.input(37) == GPIO.LOW:
				print("Door 3 is Open")
				door3image = IMAGE_OPEN
				Any_Door_Open = Any_Door_Open + 2

	if Any_Door_Open == 0:
		bgcolor = BG_COLOR_CLOSED
	if Any_Door_Open == 1:
		bgcolor = BG_COLOR_QUESTION
	if Any_Door_Open > 1:
		bgcolor = BG_COLOR_OPEN

	return render_template('doorstatus.txt',
		Refresher = No_Refresh,
		color = bgcolor, 
		door1status = door1image, 
		door2status = door2image, 
		door3status = door3image, 
		doorstatussize = imagesize, 
		door1visable = door1, 
		door2visable = door2, 
		door3visable = door3, 
		D1Name = DOOR_1_NAME, 
		D2Name = DOOR_2_NAME, 
		D3Name = DOOR_3_NAME)


@app.route('/Settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
		if request.form['ADMIN'] == ADMIN and request.form['ADMIN_PASS'] == ADMIN_PASS:
			#open text file in read mode
			AutoStart = open("/etc/rc.local", "r")
	 	
			#read whole file to a string
			AutoStartFile = AutoStart.read()
 	
			#close file
			AutoStart.close()
 
			if ENABLE_PASSWORD == "YES":
				ENABLE_PASSWORD_YES = " Checked"
				ENABLE_PASSWORD_NO = ""
			else:
				ENABLE_PASSWORD_YES = ""
				ENABLE_PASSWORD_NO = " Checked"

			if ENABLE_SIRI == "YES":
				ENABLE_SIRI_YES = " Checked"
				ENABLE_SIRI_NO = ""
			else:
				ENABLE_SIRI_YES = ""
				ENABLE_SIRI_NO = " Checked"

			return render_template('settings.txt',
				PORT = PORT,
				ENABLE_PASSWORD_YES = ENABLE_PASSWORD_YES,
				ENABLE_PASSWORD_NO = ENABLE_PASSWORD_NO,
				PASSWORD = PASSWORD,
				ENABLE_SIRI_YES = ENABLE_SIRI_YES,
				ENABLE_SIRI_NO = ENABLE_SIRI_NO,
				SIRI_PASSWORD = SIRI_PASSWORD,
				BG_COLOR_QUESTION = BG_COLOR_QUESTION,
				BG_COLOR_OPEN = BG_COLOR_OPEN,
				BG_COLOR_CLOSED = BG_COLOR_CLOSED,
				IMAGE_QUESTION = IMAGE_QUESTION,
				IMAGE_OPEN = IMAGE_OPEN,
				IMAGE_CLOSED = IMAGE_CLOSED,
				NUMBER_OF_DOORS = NUMBER_OF_DOORS,
				DOOR_1_NAME = DOOR_1_NAME,
				DOOR_2_NAME = DOOR_2_NAME,
				DOOR_3_NAME = DOOR_3_NAME,
				SENSORS_PER_DOOR = SENSORS_PER_DOOR,
				ADMIN = ADMIN,
				ADMIN_PASS = ADMIN_PASS,
				APP_PATH = APP_PATH,
				LOG_FILE = LOG_FILE,
				AutoStartFile = AutoStartFile)
		else:
			return app.send_static_file('admin_login.html')
	else:
		return app.send_static_file('admin_login.html')

@app.route('/ChangeSettings', methods=['POST'])
def ChangeSettings():

	PORT = request.form['PORT']
	ENABLE_PASSWORD = request.form['ENABLE_PASSWORD']
	PASSWORD = request.form['PASSWORD']
	ENABLE_SIRI = request.form['ENABLE_SIRI']
	SIRI_PASSWORD = request.form['SIRI_PASSWORD']
	NUMBER_OF_DOORS = request.form['NUMBER_OF_DOORS']
	DOOR_1_NAME = request.form['DOOR_1_NAME']
	DOOR_2_NAME = request.form['DOOR_2_NAME']
	DOOR_3_NAME = request.form['DOOR_3_NAME']
	SENSORS_PER_DOOR = request.form['SENSORS_PER_DOOR']
	ADMIN = request.form['ADMIN']
	ADMIN_PASS = request.form['ADMIN_PASS']

	#open text file in write mode (this will erase current file)
	ConfigFile = open("config.py", "w")

	#writes whole string to file
	ConfigFile.write('PORT = ' + PORT + '\n')
	ConfigFile.write('ENABLE_PASSWORD  = "' + ENABLE_PASSWORD + '"\n')
	ConfigFile.write('PASSWORD = "' + PASSWORD + '"\n')
	ConfigFile.write('ENABLE_SIRI = "' + ENABLE_SIRI + '"\n')
	ConfigFile.write('SIRI_PASSWORD = "' + SIRI_PASSWORD + '"\n')
	ConfigFile.write('BG_COLOR_QUESTION = "' + BG_COLOR_QUESTION + '"\n')
	ConfigFile.write('BG_COLOR_OPEN = "' + BG_COLOR_OPEN + '"\n')
	ConfigFile.write('BG_COLOR_CLOSED = "' + BG_COLOR_CLOSED + '"\n')
	ConfigFile.write('IMAGE_QUESTION = "' + IMAGE_QUESTION + '"\n')
	ConfigFile.write('IMAGE_OPEN  = "' + IMAGE_OPEN + '"\n')
	ConfigFile.write('IMAGE_CLOSED = "' + IMAGE_CLOSED + '"\n')
	ConfigFile.write('NUMBER_OF_DOORS = ' + NUMBER_OF_DOORS + '\n')
	ConfigFile.write('DOOR_1_NAME = "' + DOOR_1_NAME + '"\n')
	ConfigFile.write('DOOR_2_NAME = "' + DOOR_2_NAME + '"\n')
	ConfigFile.write('DOOR_3_NAME = "' + DOOR_3_NAME + '"\n')
	ConfigFile.write('SENSORS_PER_DOOR = ' + SENSORS_PER_DOOR + '\n')
	ConfigFile.write('ADMIN = "' + ADMIN + '"\n')
	ConfigFile.write('ADMIN_PASS = "' + ADMIN_PASS + '"\n')

	#close file
	ConfigFile.close()

	return app.send_static_file('Settings_Saved.html')


@app.route('/Settings_Save_Bootfile', methods=['POST'])
def Settings_Save_Bootfile():
	StartFile = request.form['AutoStartFile']

	#open text file in write mode (this will erase current file)
	AutoStart = open("/etc/rc.local", "w")
 
	#writes whole string to file
	AutoStart.write(StartFile)
 
	#close file
	AutoStart.close()

	return app.send_static_file('Settings_Saved.html')


@app.route('/Delete_Log_File', methods=['POST'])
def Delete_Log_File():

	#open text file in write mode (this will erase current file)
	DeleteLogFile = open("static/log.txt", "w")

	DeleteLogFile.write(datetime.now().strftime("Log File Erased -- %Y/%m/%d -- %H:%M \n"))
 
	#close file
	DeleteLogFile.close()

	return app.send_static_file('Settings_Saved.html')


@app.route('/Siri/GarageDoorStatus', methods=['GET'])
def GarageDoorStatus():
	siri_door1_message = ""
	siri_door2_message = ""
	siri_door3_message = ""
	Any_Door_Open = 0

	if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH: #Door 1 Unknown
		if SENSORS_PER_DOOR == 1:
			siri_door1_message = DOOR_1_NAME + " is open"
		else:
			siri_door1_message = DOOR_1_NAME + " is questionable"
		Any_Door_Open = 1
	else:
		if GPIO.input(16) == GPIO.LOW: # Door 1 Closed
			siri_door1_message = ""
		if GPIO.input(18) == GPIO.LOW: # Door 1 Open
			siri_door1_message = DOOR_1_NAME + " is open"
			Any_Door_Open = 1

	if NUMBER_OF_DOORS > 1:
		if GPIO.input(29) == GPIO.HIGH and GPIO.input(31) == GPIO.HIGH:
			if SENSORS_PER_DOOR == 1:
				siri_door2_message = DOOR_2_NAME + " is open"
			else:
				siri_door2_message = DOOR_2_NAME + " is questionable"
			Any_Door_Open = Any_Door_Open + 1
		else:
			if GPIO.input(29) == GPIO.LOW:
				siri_door1_message = ""
			if GPIO.input(31) == GPIO.LOW:
				siri_door2_message = DOOR_2_NAME + " is open"
				Any_Door_Open = Any_Door_Open + 1

	if NUMBER_OF_DOORS == 3:
		if GPIO.input(33) == GPIO.HIGH and GPIO.input(37) == GPIO.HIGH:
			if SENSORS_PER_DOOR == 1:
				siri_door3_message = DOOR_3_NAME + " is open"
			else:
				siri_door3_message = DOOR_3_NAME + " is questionable"
			Any_Door_Open = Any_Door_Open + 1
		else:
			if GPIO.input(33) == GPIO.LOW:
				siri_door3_message = ""
			if GPIO.input(37) == GPIO.LOW:
				siri_door3_message = DOOR_1_NAME + " is open"
				Any_Door_Open = Any_Door_Open + 1

	siri_message = ""
	if Any_Door_Open == 0:
		return 'All Doors are Closed'
	if Any_Door_Open != 0:

		if siri_door1_message != "":
			siri_message = siri_door1_message
		if siri_door2_message != "":
			if siri_message == "":
				siri_message = siri_door2_message
			else:
				siri_message = siri_message + ', ' + siri_door2_message
		if siri_door3_message != "":
			if siri_message == "":
				siri_message = siri_door3_message
			else:
				siri_message = siri_message + ', ' + siri_door3_message

		return siri_message


@app.route('/Siri/Garage', methods=['POST'])
def GarageSiri():
	ps = request.form['ps']
	what_door = request.form['door']
	dowhat = request.form['dowhat']


	if ps == SIRI_PASSWORD:
		logfile = open("static/log.txt","a")
		logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- " + request.environ['REMOTE_ADDR'] + " -- Garage Door Operated via Siri  \n"))
		logfile.close()

		if what_door == "Door1" and dowhat == "Open":
			if GPIO.input(16) == GPIO.LOW:
				print("Door 1 is currently Closed, let's open it.")
				GPIO.output(7, GPIO.LOW)
				time.sleep(1)
				GPIO.output(7, GPIO.HIGH)
				return 'Garage Door Opening'
			if GPIO.input(16) == GPIO.HIGH:
				print("Garage is already open, do nothing.")
				return 'Door 1 is already open'
		if what_door == "Door1" and dowhat == "Close":
			if GPIO.input(18) == GPIO.LOW:
				print("Garage is currently Open, let's close it.")
				GPIO.output(7, GPIO.LOW)
				time.sleep(1)
				GPIO.output(7, GPIO.HIGH)
				return 'Garage Door Closing'
			if GPIO.input(18) == GPIO.HIGH:
				print("Garage is already closed, do nothing.")
				return 'Door 1 is already closed'


		if what_door == "Door2" and dowhat == "Open":
			if GPIO.input(29) == GPIO.LOW:
				print("Door 2 is currently Closed, let's open it.")
				GPIO.output(11, GPIO.LOW)
				time.sleep(1)
				GPIO.output(11, GPIO.HIGH)
				return 'Garage Door Opening'
			if GPIO.input(29) == GPIO.HIGH:
				print("Garage is already open, do nothing.")
				return 'Door 2 is already open'
		if what_door == "Door2" and dowhat == "Close":
			if GPIO.input(31) == GPIO.LOW:
				print("Garage is currently Open, let's close it.")
				GPIO.output(11, GPIO.LOW)
				time.sleep(1)
				GPIO.output(11, GPIO.HIGH)
				return 'Garage Door Closing'
			if GPIO.input(31) == GPIO.HIGH:
				print("Garage is already closed, do nothing.")
				return 'Door 2 is already closed'

		if what_door == "Door3" and dowhat == "Open":
			if GPIO.input(33) == GPIO.LOW:
				print("Door 2 is currently Closed, let's open it.")
				GPIO.output(13, GPIO.LOW)
				time.sleep(1)
				GPIO.output(13, GPIO.HIGH)
				return 'Garage Door Opening'
			if GPIO.input(33) == GPIO.HIGH:
				print("Garage is already open, do nothing.")
				return 'Door 2 is already open'
		if what_door == "Door3" and dowhat == "Close":
			if GPIO.input(37) == GPIO.LOW:
				print("Garage is currently Open, let's close it.")
				GPIO.output(13, GPIO.LOW)
				time.sleep(1)
				GPIO.output(13, GPIO.HIGH)
				return 'Garage Door Closing'
			if GPIO.input(37) == GPIO.HIGH:
				print("Garage is already closed, do nothing.")
				return 'Door 2 is already closed'

	else:
		return 'We have a problem'

@app.route('/stylesheet.css')
def stylesheet():
	return app.send_static_file('stylesheet.css')

@app.route('/Log')
def logfile():
	return app.send_static_file('log.txt')

@app.route('/images/<path:subpath>')
def SiriPics(subpath):
	return app.send_static_file('images/' + subpath)

@app.route('/page/<sendpage>')
def page(sendpage):
	return app.send_static_file(sendpage)

if __name__ == '__main__':
	app.run(debug=True, host=ip_address, port=PORT)
