#!/usr/bin/python3

#################################################################
# TABLE CLASS
#
# Version: 4.0
# Project: Testing Bench fot Chemical Lab
# Company: Nanosonics
# Author:  Ahmed ALi Omer Ali
# Date:    7/11/2018
#
#
# Comments:
#   This class generates a table to be integrated inside a GUI
#
#   The table is configured to support the requirements of the
#   GUI class due to resolutions and other possible error, it
#   may need to be changed.
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



class Table(tk.Frame):

    def __init__(self, parent,nCol, labels):
        self.labels = labels
        tk.Frame.__init__(self, parent)
        self.CreateUI(nCol)
        self.grid(sticky="ns")
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
        self.parent = parent
        self.currentValues = '22'

    def getColumns(self):
        columns = []
        for i in range(15):
            columns.append(self.labels[i+1])
        return columns

    def CreateUI(self,nCol):
#        size=[70,100,60,60,80,110,80,110,80,110,80,110,70,70,70,70]
        size=[60,120,60,60,60,90,60,90,60,90,60,90,65,65,65,65]
        self.tv = ttk.Treeview(self)
        columns = self.getColumns()
        self.tv['columns'] = columns
        self.tv.configure(height=nCol)
        self.tv.heading("#0", text=self.labels[0], anchor='center')
        self.tv.column("#0", anchor="center", width = size[0])
        for i in range(15):
            self.tv.heading(columns[i], text=columns[i])
            self.tv.column(columns[i], anchor="center", width = size[i+1])
        self.tv.bind('<ButtonRelease-1>',self.tableSelectedRow)
        self.tv.pack()
        self.treeview = self.tv

    def LoadTable(self):
        self.treeview.insert('', 'end', text="First", values=(self.getColumns()), tags=('oddrow'))
        
    def LoadTable2(self):
        self.treeview.insert('', 'end', text="First", values=(self.getColumns()),tags=('evenrow') )

    def LoadTableData(self,stage, data):
        self.treeview.insert('', 'end', text=str(stage), values=(data), tags=('oddrow'))
        
    def LoadTable2Data(self,stage, data):
        self.treeview.insert('', 'end', text=str(stage), values=(data), tags=('evenrow'))
    
    def setColors(self):
        self.treeview.tag_configure('oddrow', background='white')
        self.treeview.tag_configure('evenrow', background='#E8E4E4')

    def tableSelectedRow(self, a):
        self.currentValues = self.tv.item(self.tv.selection())

