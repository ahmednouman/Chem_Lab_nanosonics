#!/usr/bin/python3

############################################################
# DOUT CLASS
#
# Project: Testing Bench fot Chemical Lab
# Company: Nanosonics
# Author:  Ahmed Ali Omer Ali
# Date:    07/11/2018
#
#
# Comments:
#   This calls defines a Digital Output and give to it
#   functionality. Set on, Set off and delete
#
############################################################


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


class Dout():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin,GPIO.OUT)
        
    def setOn(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(self.pin,GPIO.HIGH)
        
    def setOff(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(self.pin,GPIO.LOW)
