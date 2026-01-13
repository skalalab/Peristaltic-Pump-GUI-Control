# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 11:51:11 2025

@author: aisaak

This program allows users to choose how long they want the program to run,
how often they want to take samples, and how much volume to dispense 
from a parastaltic pump at a specified rate

"""
import serial
import time
from datetime import datetime, timedelta
class Pump_control_timed:
    def __init__(self):
        super().__init__()
        # creates a serial prot object to open  a serial with an adruino on COM#
        self.arduino = serial.Serial(port = 'COM1', baudrate=9600, timeout = .1)
        
        #-----------------main parameters------------------------#
        self.runTime = 30.0 # seconds - how long the program should run
        self.interval = 10.0 # seconds - serial vals sent to arduino every interval seconds
        self.amountDispensed = 0.2 #mL - amount of liquid to be dispensed
        #------------------------parameters----------------------#
        self.rate = 0.38 # rate in mL/s, this value does not change the speed of the pump
        self.toArduino = 70.0 # serial val sent to arduino to turn on
        #-----------------calculated-values----------------------#
        self.pumpOn = 0.0 # how long the pump stays on to pump an amount of liquid
        self.waitTime = 0.0 # how long the program has to wait before sending serial vals to arduino
        self.timesRun = 0.0 # how many times the pump will turn on 
        
    
    # this method sends a numerical value (serialVal) to a serial port
    def writeTo(self, serialVal):
        #print("sending ", serialVal, "to arduino")
        #converts the inputted value back to string
        serialVal = str(serialVal) 
        #sends value to arduino as byted encoded with utf-8
        self.arduino.write(bytes(serialVal, 'utf-8'))
        time.sleep(0.05)
        
    # returns a value read from the serial port
    def readFrom(self):
        #decodes the serial output from arduino
        value = self.arduino.readline().decode('utf-8')
        return value
    
    # This method takes input from a GUI and calculates and sets all of 
    # values. Should be used before running the pump
    def set_vals (self, runTime, interval, amountDispensed, rate):
      self.runTime = int(runTime) #in s
      self.interval = int(interval) #in s
      self.amountDispensed = int(amountDispensed) #in ul
      self.rate = (self.rate * 1000) #uL/s
      if self.rate != 0:  
          self.pumpOn = self.amountDispensed / self.rate  
      else:
          raise ValueError ("the rate cannot be 0")
      self.waitTime = self.interval - self.pumpOn 
      self.timesRun = int(runTime / interval)      
      
    def validateInput(self):
        # checks if the specified interval can be split evenly across the run time
        if(not self.runTime % self.interval == 0):
            print("The overall time cannot be divided evenly into the entered intervals.\n")
            if(self.runTime < self.interval):
                raise ValueError("time interval cannot be larger than run time")
                
        # if(toArduino is None or not 225 >= toArduino >= 0):
        #     raise ValueError("Invalid speed sent to Arduino")
    
    # This method prints the start and end time of the run and how many samples
    # will be taken over that period of time            
    def printTime(self):
        startTime = datetime.now().replace(microsecond=0)
        #currentInterval = startTime
        endTime = startTime + timedelta(seconds = self.runTime)
        print("start: ", startTime)
        print("end: ", endTime)
        print(self.timesRun, "samples will be taken over the time period")
        
    def printCurrentTime():
        print(datetime.now())
    
    # Runs the last iteration of the pump turning on and off.
    # This is seperated to not have a waiting period after it's done running.
    def runLast(self):
        print("sending ", self.toArduino, "to arduino")
        self.writeTo(self.toArduino)
        time.sleep(0.5) #pause for aruduino to respond
        print("Read from Arduino:", self.readFrom())
        time.sleep(self.pumpOn) #time the pump is on 
       
    # Prints the time the program stopped running,
    # sends 0 to arduino to stop the pump, and
    # sets the value toArduino to 0
    def endRun(self):
        print ("end at", datetime.now() )
        print("pump done running, turning off pump")
        # once the pump is stopped the serial is closed unitl the program runs again
        self.toArduino = 0
        self.writeTo(0)
        
    # Closes the serial port. This helps prevent busy COM port errors
    def closeSerial(self):
        print("program finished, closing serial port")
        time.sleep(1)#if pump doesn't shut off when 0 is entered this should be a larger value
        self.arduino.close()#closes the serial port to prevent busy serial port issues
    