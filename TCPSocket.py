#!/usr/bin/env python

#-----------------------------------------------------------
# File name   : TCPSocket.py
# Description : This file will send .csv file from Raspberry Pi to client computer
# Author      : Maria Mercid L. Sukati	
# E-mail      : mariamercidlangbid@gmail.com
# Date        : 6 Nov 2017
#-----------------------------------------------------------

import time
import socket               			# Import socket module
import sys
import os

HOST = ''								# Uncomment if you want to receive file
#HOST = '192.168.1.104'					# Uncomment if you want to send file
PORT = 8080
BUFSIZ = 1024							#Size of the buffer

class TCPSocket(object):			
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
		else:
			self.sock = sock


	def connect(self, host, port):
		print("Connecting...")		
		self.sock.connect((host, port))


	def send(self, filename):
		print("Sending...")
		data = None

		try:
			with open(filename, 'r') as file:
				readFile = file.read(BUFSIZ)			
				while(readFile):				
					self.sock.sendall(readFile)
					readFile = file.read(BUFSIZ)		
				self.sock.sendall("\$End")		
				print("Done sending.")	
				data = self.sock.recv(BUFSIZ)
		except socket.error as msg:
			print(msg)
		finally:
			self.sock.close()	
			return data


	def recv(self):
		return self.sock.recv(BUFSIZ)


	def receive(self, host, port):		
		self.sock.bind((host, port))					# Bind the IP Address to the port
		self.sock.listen(1)								# Wait for 1 client connection
		
		clientSocket, cAddr = self.sock.accept()		# Establish connection with the client

		print("Got connection from ", cAddr)
		print("Receiving file...")		

		timeStr = time.strftime("%d%m%Y")	
		filename = "stocklist_" + timeStr + ".csv"		# The filename has postfix with the date it was created

		while True:
			try:
				clientData = clientSocket.recv(BUFSIZ)
				with open(filename, 'w') as file:
					while (clientData != "\$End"):
						file.write(clientData)
						clientData = clientSocket.recv(BUFSIZ)
					print("Receiving complete.")
				if clientData == "\$End":
					clientSocket.sendall("OK")
					break
			except socket.error as msg:
				print(msg)
				break

		clientSocket.shutdown(socket.SHUT_WR)		
		clientSocket.close()					# Close the connection	


# Use this to test receive file
# print("Waiting for connection...")
# recvSocket = TCPSocket()
# recvSocket.receive(HOST, PORT)


# Use this to test send file
# sendSocket = TCPSocket()
# sendSocket.connect(HOST, PORT)
# sendSocket.send("Rubric_3.txt")
# sendSocket.close()
