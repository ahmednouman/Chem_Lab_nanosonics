#!/usr/bin/python3

#################################################################
# TEST CLASS            
#
# Project: Testing Bench fot Chemical Lab
# Company: Nanosonics
# Author:  Ahmed Ali Omer Ali
# Date:    07/11/2018
#
# Comments:
#   This class generates a sequence of on/off commands to verify
#   the board is working properly. 
#
#################################################################



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


class Test():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        LedList=[3,5,7,29,31,26,24,21,19,23,32,33,8,10,36,11,12,35,38,40,15,16,18,22,37,13]  

        for i in LedList:
            GPIO.setup(i,GPIO.OUT)

        try:
            for i in LedList:
                GPIO.output(i,GPIO.HIGH)
                time.sleep(.05)
                GPIO.output(i,GPIO.LOW)
                time.sleep(.05)
        except:
            print ("An error occurred")

        finally:
            GPIO.cleanup()

