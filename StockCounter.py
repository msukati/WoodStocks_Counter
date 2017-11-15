#!/usr/bin/env python

#-----------------------------------------------------------
# File name   : StockCounter.py
# Description : This class is able to read the contents of a csv file and display it.
# Author      : Maria Mercid L. Sukati	
# E-mail      : mariamercidlangbid@gmail.com
# Date        : 7 Nov 2017
#-----------------------------------------------------------
from __future__ import print_function

# System class
import csv
import os
import sys
import time

# User class
import TCPSocket
import LED
import Keypad

# Constants
HOST = '192.168.1.102'										# IP Address of the computer where you want to send the file
PORT = 8080

# The main function
def main():
	os.system("cls||clear")									# cls for Windows and clear for Linux. This will clear the screen.
	runStockCounter("stocklist.csv")

# This function contains the core functionality of the StockCounter class 
def runStockCounter(filename):
	try:
        if os.stat(filename).st_size == 0: 				# Checks if file is empty
            print("Terminating program. File is empty!!!")
            sys.exit(1)
                            
		while True:
			with open(filename, 'r') as rfile:					# Opens the file
				readCSV = csv.reader(rfile, delimiter=',')		# Returns a reader object that will iterate through the lines of the file
				readCSV.next()									# Skips the header row and points to the first item row

				for row in readCSV:
					displayItem(row)							
					print("\n")
					
					newCount = ""
					while (newCount.isdigit() == False):
						print("Enter NEW Count: ", )
						newCount = useKeypad()				# User should enter a digit or it will keep on asking a new count
						print(newCount)
						time.sleep(0.5)   					# This is needed so that the loop will be displayed properly
					
					writeFile(row, int(newCount))					
					os.system("cls||clear")						
						
			# Give the user an option to edit the file again or send directly										
			option = ""
			while (option != "A" and option != "B"):
				print("\nPress A to send file. Press B to edit the stock count again. ")	# User should enter A or B or it will keep on asking an option
				option = useKeypad()
				print(option)			
				time.sleep(0.3)
			os.system("cls||clear")	


			os.remove(filename)							# After the new stock count was written to the temporary file, remove the old file			
			os.rename("temp.csv", filename)				# Rename the temporary file to stocklist.csv which will now contain the updated stock count
			
			if (option.upper() == "A"):				
				sendTCPSocket = TCPSocket.TCPSocket()
				sendTCPSocket.connect(HOST, PORT)
				msg = sendTCPSocket.send(filename)
								
				print("Message: "+ str(msg))

				#Activate the LED
				setLED = LED.LED()
				if msg == "OK":					# Turn on Green LED for 5 sec to indicate sending OK
					setLED.setGreen(True)
					setLED.setRed(False)
				else:							# Turn on Red LED for 5 sec to indicate sending NOK
					setLED.setGreen(False)
					setLED.setRed(True)

				setLED.destroy()

				break # if (option == "A")			

	except IOError as e: 									# Catch the error in case the file is missing.
		print('Could not open file {}! '.format(filename), e)
		sys.exit(1)

	except KeyboardInterrupt:
		os.remove(filename)							# After the new stock count was written to the temporary file, remove the old file			
		os.rename("temp.csv", filename)				# Rename the temporary file to stocklist.csv which will now contain the updated stock count

# This will display the item information to the user
def displayItem(row):		
	print("Code: {}".format(row[0]))
	print("Description: {}".format(row[1]))
	print("Current Count: {}".format(row[2]))
	print("On Order: {}".format(row[3]))	


def useKeypad():
	kp = Keypad.Keypad()
	list = ['']
    digit = None
    num = None

    # Loop while waiting for a keypress
    while True:        
        digit = kp.getKey()
        if digit != None and digit != '*' and digit != "A" and digit != "B":
            list.append(str(digit))
            time.sleep(0.5)
            digit = None        
        elif digit == '*':
            num = ''.join(list)                
            break
        elif digit == "A" or digit == "B":
            num = digit
            break

    return num

# This will create the new file containing the new stock count
def writeFile(row, value):	
	f = os.path.exists("temp.csv")							# This will check if the temp.csv is already created or not.
	mode = "a"

	if f == False:
		mode = "w"

	with open("temp.csv", mode) as wfile:
		writeCSV = csv.writer(wfile, delimiter=',', lineterminator='\n')

		if mode == "w":	# This part is only evaluated if the file is newly created
			writeCSV.writerow(["Item Code", "Item Description", "Current Count", "On Order"])

		writeCSV.writerow([row[0], row[1], value, row[3]])


if __name__ == "__main__": main()		