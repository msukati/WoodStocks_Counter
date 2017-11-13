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
HOST = '192.168.1.101'										# Use this if you want to send file
PORT = 8080

# The main function
def main():
	os.system("cls||clear")									# cls for Windows and clear for Linux. This will clear the screen.
	runStockCounter("stocklist.csv")

# This function contains the core functionality of the StockCounter class 
def runStockCounter(filename):
	try:
		while True:
			with open(filename, 'r') as rfile:					# Opens the file
				readCSV = csv.reader(rfile, delimiter=',')		# Returns a reader object that will iterate through the lines of the file
				
				if readCSV == None:   #Terminate the program when file is empty
                    print("File is empty!!!")
                    sys.exit(1)
                                
				readCSV.next()									# Skips the header row and points to the first item row

				for row in readCSV:
					displayItem(row)							
					print("\n")

					#newCount = int(input("Enter NEW Count: "))	# Remove this line after Keypad class is tested
					# Use this for Keypad class
					print("Enter NEW Count: ")
					newCount = useKeypad()
					print(newCount)
					time.sleep(0.5)   							#This is needed so that the loop will be displayed properly
					
					writeFile(row, newCount)					
					os.system("cls||clear")						
			
			os.remove("stocklist.csv")							# After the new stock count was written to the temporary file, remove the old file			
			os.rename("temp.csv", "stocklist.csv")				# Rename the temporary file to stocklist.csv which will now contain the updated stock count

			# Give the user an option to edit the file again or send directly							
			print(r"\nSend the file to the server[A/B] A for Yes, B for No: ") # If A, send the csv file. If B, go back to edit the file again
			option = useKeypad()
			print(option)
			time.sleep(0.5)
			if (option.upper() == "A"):				
				sendTCPSocket = TCPSocket.TCPSocket()
				sendTCPSocket.connect(HOST, PORT)
				msg = sendTCPSocket.send("stocklist.csv")
				#msg = "NOK"
				
				print("Message from receiver is " + msg)

				#Activate the LED
				setLED = LED.LED()

				if msg == "OK":					# Turn on Green LED for 2 sec to indicate sending OK
					setLED.setGreen(True)
					setLED.setRed(False)
				else:							# Turn on Red LED for 2 sec to indicate sending NOK
					setLED.setGreen(False)
					setLED.setRed(True)

				setLED.destroy()

				break # if (option == "y")			

	except IOError as e: 									# Catch the error in case the file is missing.
		print('Could not open file {}! '.format(filename), e)
		sys.exit(1)

# This will display the item information to the user
def displayItem(row):		
	print("Code: {}".format(row[0]))
	print("Description: {}".format(row[1]))
	print("Current Count: {}".format(row[2]))
	print("On Order: {}".format(row[3]))	


def useKeypad():
	#pass
	kp = Keypad.Keypad()
	list = ['']
        digit = None
        num = None

    # Loop while waiting for a keypress
        while True:        
            digit = kp.getKey()
            if digit != None and digit != '*':
                list.append(str(digit))
                time.sleep(0.5)
                digit = None        
            elif digit == '*':
                num = ''.join(list)                
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