#!/usr/bin/python3

#########################################################
# RASPI CLASS
#
# Project: Testing Bench fot Chemical Lab
# Company: Nanosonics
# Author:  Manuel Bernal Lecina
# Date:    07/11/2018
#
# Comments:
#   Class to structure the functionality of the Raspberry
#   board.
#
#   It would generate a Board object and listen to the
#   value of the given flags to know if it has to run,
#   pause, stop or skip the stage sent to it.
#
#########################################################


#IMPORTS
import RPi.GPIO as GPIO

import time
import datetime

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

from pathlib import Path

from StageClass import Stage
from PumpClass import Pump
from DoutClass import Dout




class RasPi():
    
    #CONSTANTS
    #-----------------------------------------------------------------------
    
    BRDPIN = 29                                 #POWER PIN RASPI 
    PUMPPINLIST = [11,36,38,40,16,18,37,13]     #LIST OF PINS FOR PMW
#    PUMPPINLIST = [24,21,19,23,32,33,12,35]    # grounp 2 can be separate or join
    DOUTPINLIST = [31,15,26,22]                 #LIST OF PINS FOR DIGITAL OUTPUT


    #CONSTRUCTORS
    #------------------------------------------------------------------------
            
    #INIT METHOD
    def __del__(self):
        self.end()
    
    def __init__(self):
        self.code = 13
        self.power = False
        self.pumps = []
        self.douts = []
        self.stages = []
        self.sCount = 0
        self.data = []
        self.flag = False
        self.pause = False
        self.next = False
        self.hz = 100
        self.HzValues=[100,100,100,100]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        try:
            #INITIALIZE GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.BRDPIN,GPIO.OUT)

            #INITILIZE PWM
           # for i in range (8):
                #GPIO.setup(self.PUMPPINLIST[i],GPIO.OUT)
             #   self.pumps.append(Pump(self.PUMPPINLIST[i],self.hz))
            
            self.pumps.append(Pump(self.PUMPPINLIST[0],self.HzValues[0]))
            self.pumps.append(Pump(self.PUMPPINLIST[1],self.HzValues[0]))

            self.pumps.append(Pump(self.PUMPPINLIST[2],self.HzValues[1]))
            self.pumps.append(Pump(self.PUMPPINLIST[3],self.HzValues[1]))

            self.pumps.append(Pump(self.PUMPPINLIST[4],self.HzValues[2]))
            self.pumps.append(Pump(self.PUMPPINLIST[5],self.HzValues[2]))

            self.pumps.append(Pump(self.PUMPPINLIST[6],self.HzValues[3]))
            self.pumps.append(Pump(self.PUMPPINLIST[7],self.HzValues[3]))
            #INITILIZE DOUTS
            for i in range (4):
                GPIO.setup(self.DOUTPINLIST[i],GPIO.OUT)
                self.douts.append(Dout(self.DOUTPINLIST[i]))

            GPIO.output(self.BRDPIN, GPIO.HIGH)
            self.power = True

            self.stag = Stage(self.pumps,self.douts)
            
        except Exception as err:
            print(err.__class__)
            print(err)

    def setAll(self,value, parent, minTimer, secTimer, flag, pauseF, nextF, config, HzValues):
        self.flag = flag.value
        self.pause = pauseF.value
        self.next = nextF.value

        if(HzValues != self.HzValues):
            self.changeHz(HzValues)
            self.HzValues = HzValues
        
        try:
            self.values = value
            
            if (len(self.values) == 15):
                print(self.values)
                print('')
                self.stag.setValues(self.values, config)

                self.timeSteps = int(self.values[1])*600 + int(self.values[2])*10
                
                self.mins = int(self.values[1])
                self.secs = int(self.values[2])
                self.count = 0
                minTimer.config(text=str(self.mins))
                secTimer.config(text=str(self.secs))

                for i in range(self.timeSteps):
                    self.flag = flag.value
                    self.pause = pauseF.value
                    self.next = nextF.value
                    

                    input_state = GPIO.input(7)
                    if input_state == False:
                        for i in range (8):
                            GPIO.setup(self.PUMPPINLIST[i],GPIO.OUT)
                            GPIO.output(self.PUMPPINLIST[i],0)
                        self.flag = False
                        



                    
                    if (self.next):
                        self.nextFlag.setValue(False)

                    else:
                        #PAUSE LOOPS
                        if(self.pause): 
                            self.stag.setZeros()
                            
                        while (self.pause):
                            self.flag = flag.value
                            self.pause = pauseF.value
                            self.next = nextF.value
                            if(self.next):
                                self.flag=False
                                break
                            if not(self.flag):
                                break
                            parent.update()
                            time.sleep(.01)
                            
                        if not (self.pause):
                            self.stag.setValues(self.values, config)

                        if (self.flag):
                            self.count += 1
                            if(self.count % 10 == 0):
                                self.secs -= 1 
                                minTimer.config(text=str(self.mins))
                                secTimer.config(text=str(self.secs))

                            if (self.secs == 0):
                                self.secs = 60
                                self.mins -= 1
                                
                            parent.update()
                            time.sleep(.1)

                                                     
                        

            elif (len(self.values) != 1):
                #print("Warning!!--> Error in text file...")
                time.sleep(10)

            #self.brdOff()
            
        except KeyboardInterrupt:
            self.end()
            
        except Exception as err:
            print('not ok')
            print(err.__class__)
            print(err)
        finally:
            self.stag.setZeros()
            #CLEAR GPIO
            #self.end()


    #METHODS
    #------------------------------------------------------------------------
    #CHANGE Hz
    def changeHz(self, HzValues):
        #GPIO.cleanup()

        try:
            #INITIALIZE GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.BRDPIN,GPIO.OUT)

            #INITILIZE PWM
            #for i in range (8):
                #GPIO.setup(self.PUMPPINLIST[i],GPIO.OUT)
             #   self.pumps.append(Pump(self.PUMPPINLIST[i],hz))

            self.pumps.append(Pump(self.PUMPPINLIST[0],HzValues[0]))
            self.pumps.append(Pump(self.PUMPPINLIST[1],HzValues[0]))

            self.pumps.append(Pump(self.PUMPPINLIST[2],HzValues[1]))
            self.pumps.append(Pump(self.PUMPPINLIST[3],HzValues[1]))

            self.pumps.append(Pump(self.PUMPPINLIST[4],HzValues[2]))
            self.pumps.append(Pump(self.PUMPPINLIST[5],HzValues[2]))

            self.pumps.append(Pump(self.PUMPPINLIST[6],HzValues[3]))
            self.pumps.append(Pump(self.PUMPPINLIST[7],HzValues[3]))
            print (HzValues)

            #INITILIZE DOUTS
            for i in range (4):
                #GPIO.setup(self.DOUTPINLIST[i],GPIO.OUT)
                self.douts.append(Dout(self.DOUTPINLIST[i]))

            GPIO.output(self.BRDPIN, GPIO.HIGH)
            self.power = True

            self.stag = Stage(self.pumps,self.douts)
                
        except Exception as err:
            print(err.__class__)
            print(err)
    
       
    #SETUP BOARD GPIO METHOD
    def setupBrd(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.BRDPIN,GPIO.OUT)
        
    #TURN ON BOARD METHOD
    def brdOn(self):
        #global power
        GPIO.output(self.BRDPIN, GPIO.HIGH)
        self.power = True
        
    #TURN OFF BOARD METHOD
    def brdOff(self):
        #global power
        GPIO.output(self.BRDPIN, GPIO.LOW)
        self.power = False
        
    #CLEAR GPIO METHOD
    def end(self):
        GPIO.cleanup()
