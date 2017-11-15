#!/usr/bin/env python

#-----------------------------------------------------------
# File name   : LED.py
# Description : Set the status of Green and Red LED
# Author      : Maria Mercid L. Sukati  
# E-mail      : mariamercidlangbid@gmail.com
# Date        : 10 Nov 2017
#-----------------------------------------------------------

import RPi.GPIO as GPIO
import time

class LED(object):
    def __init__(self, LedPin1=29, LedPin2=31):
        self.LedPin1 = LedPin1
        self.LedPin2 = LedPin2

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)                    # Numbers pins by physical location
        GPIO.setup(self.LedPin1, GPIO.OUT)          # Set pin mode as output
        GPIO.output(self.LedPin1, GPIO.HIGH)        # Set pin to high(+3.3V) to off the led
        GPIO.setup(self.LedPin2, GPIO.OUT)          # Set pin mode as output
        GPIO.output(self.LedPin2, GPIO.HIGH)        # Set pin to high(+3.3V) to off the led

    def setGreen(self, status):   # Pin 11
        if status == True:
            GPIO.output(self.LedPin1, GPIO.LOW)      # LED ON
            time.sleep(5)
            GPIO.output(self.LedPin1, GPIO.HIGH)     # LED OFF after 5 sec
        else:    
            GPIO.output(self.LedPin1, GPIO.HIGH)     # LED OFF

    def setRed(self, status):     # Pin 12
        if status == True:
            GPIO.output(self.LedPin2, GPIO.LOW)      # LED ON
            time.sleep(5)
            GPIO.output(self.LedPin2, GPIO.HIGH)     # LED OFF after 5 sec
        else:    
            GPIO.output(self.LedPin2, GPIO.HIGH)     # LED OFF


    def destroy(self):
        self.setGreen(False)
        self.setRed(False)
        GPIO.cleanup()


#Test the LED class
# if __name__ == '__main__':
#     setLED = LED()
#     #Turn ON Green LED
#     setLED.setGreen(True)
#     setLED.setRed(False)
#     #Turn ON Red LED
#     setLED.setGreen(False)
#     setLED.setRed(True)
#     setLED.destroy()